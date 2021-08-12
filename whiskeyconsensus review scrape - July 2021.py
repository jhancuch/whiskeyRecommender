#!/usr/bin/env python
# coding: utf-8

# In[1]:


# load libraries

import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# In[2]:


# load the url associated with each review page

datUrl = pd.read_pickle('./whiskeyconsensus-reviews-urls-July-2021.pkl')


# In[3]:


# scrape each of the reviews for the desired information

nameList = []
colorList = []
noseList = []
palateList = []
finishList = []

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
}


for url in datUrl['reviewUrl']:
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    soupTitleTemp = str(soup).replace("\n", "")
    nameTemp = re.findall('<h1 class="page-header-title clr" itemprop="headline">.*</h1>', soupTitleTemp)
    if len(nameTemp) > 0 :
        name = nameTemp[0].replace('<h1 class="page-header-title clr" itemprop="headline">', '').replace('</h1>', '')
        nameList.append(name)
    else:
        name = 'NA'
        nameList.append(name)
        
    soup_refined = str(soup.find_all('div', class_ = 'elementor-text-editor elementor-clearfix')).replace("\n", "")
    
    colorInfoTemp = re.findall("Color</h3><p>.*</p><h3>Nose", soup_refined)
    if len(colorInfoTemp) > 0:
        colorInfo = colorInfoTemp[0].replace('Color</h3><p>', '').replace('</p><h3>Nose', '')
        colorList.append(colorInfo)
    else:
        colorInfo = 'NA'
        colorList.append(colorInfo)
    
    noseInfoTemp = re.findall("Nose</h3><p>.*</p><h3>Palate", soup_refined)
    if len(noseInfoTemp) > 0:
        noseInfo = noseInfoTemp[0].replace('Nose</h3><p>', '').replace('</p><h3>Palate', '')
        noseList.append(noseInfo)
    else:
        noseInfo = 'NA'
        noseList.append(noseInfo)
    
    palateInfoTemp = re.findall("Palate</h3><p>.*</p><h3>Finish", soup_refined)
    if len(palateInfoTemp) > 0 :
        palateInfo = palateInfoTemp[0].replace('Palate</h3><p>', '').replace('</p><h3>Finish', '')
        palateList.append(palateInfo)
    else:
        palateInfo = 'NA'
        palateList.append(palateInfo)
    
    finishInfoTemp = re.findall("Finish</h3><p>.*</p><h3>", soup_refined)
    if len(finishInfoTemp) > 0:
        finishInfo = finishInfoTemp[0].replace('Finish</h3><p>', '').replace('</p><h3>', '')
        finishList.append(finishInfo)
    else:
        finishInfo = 'NA'
        finishList.append(finishInfo)
        
    time.sleep(10)

datRawReviews = pd.DataFrame()
datRawReviews['Name'] = nameList
datRawReviews['Color'] = colorList
datRawReviews['Nose'] = noseList
datRawReviews['Palate'] = palateList
datRawReviews['Finish'] = finishList

print(datRawReviews.head())


# In[4]:


# merge scraped information with url information

datRawReviews1 = pd.concat([datRawReviews, datUrl.reindex(datRawReviews.index)], axis=1)


# In[5]:


# subset any observations with NA
pd.set_option("display.max_rows", None, "display.max_columns", None)

datRawReviews2 = datRawReviews1[(datRawReviews1["Color"] != "NA") & (datRawReviews1["Nose"] != "NA") & (datRawReviews1["Palate"] != "NA") & (datRawReviews1["Finish"] != "NA")]

datRawReviewsUpdate = datRawReviews1[(datRawReviews1["Color"] == "NA") | (datRawReviews1["Nose"] == "NA") | (datRawReviews1["Palate"] == "NA") | (datRawReviews1["Finish"] == "NA")]

print(datRawReviews2.count())
print(datRawReviewsUpdate.count())


# In[6]:


# put in the correct information by hand
print(datRawReviewsUpdate["reviewUrl"])

newColorCol = ["Rust Orange", "Mahogany", "Light Golden", "Dark Mahogany", "Amber", "Dark copper", "Dark Amber", "Brown", 
               "Dark Amber", "Dark Mahogany", "Dark Copper", "Brown", "Amber", "Golden Amber", "Dark Mahogany", "Light Copper", 
               "Burnt Copper", "Light Amber", "Dark Copper/Rust", "Dark Copper", "Dark Copper", "Dark Copper", "Amber", 
               "Dark Mahogany", "Dark Amber Red","Light rust/copper", "Spring Honey", "Amber", "Medium Amber", "Light Amber", 
               "Burnt Orange", "Golden Amber", "Dry Straw", "Dark Gold", "Medium Gold", "Amber", "Light Copper", "Dark Copper", 
               "Light Amber", "Medium Copper", "Medium Amber", "Deep Amber", "Medium Amber", "Medium Amber", "Burnt Orange", 
               "Golden Amber", "Dark Caramel/Maple Syrup", "Medium Amber", "Deep Amber", "Amber", "Light Amber", "Deep Gold", 
               "Medium Amber", "Medium Gold", "Light Copper", "Medium Amber", "Dark Caramel", "Deep Gold", "Caramel", 
               "Light Gold", "Medium Copper", "Medium Amber", "Medium Gold", "Medium Gold", "Rust / Copper", "Rich Amber", 
               "Golden Amber", "Amber", "Deep Amber", "Medium Copper", "Medium Amber", "Light Copper", "Medium Copper", 
               "Light Copper", "Medium Gold", "Light Copper", "Yellow Gold", "Medium Gold", "Light Amber", "Light Caramel", 
               "Honey", "Dark Gold", "Medium Copper", "Golden Amber", "Golden Amber", "Medium Copper", 
               "Light Amber with hints of bright Orange", "Medium Gold", "Honey", "Straw/Bronze", "Light Gold", "Medium Gold", 
               "Orange/Copper Rust", "Golden Mahogany", "Light Gold", "Dark Gold", "Wet Hay", "Light Copper", "Light Amber", 
               "Medium Gold", "Dry Straw", "Amber", "Light Gold", "Straw", "Copper", "Light honey"]

newNoseCol = ["The nose is pretty well balanced, with the most dominate scent being orange peel. Caramel and a beautiful rye spice marry well with each other to bring both heat and sweetness. An almost vegetal scent, like steamed cauliflower gives it a pleasant uniqueness and rounds everything out. The nose is definitely powerful in alcohol content, enough to where it highlights all of the scents without the ethanol being too powerful to overcome.", 
              "Sweetness and flint hits you in the face like a smack. Rose water and a perfume, I believe I am smelling a rosewater smell. Notes of gunpowder and hot stones by a river side are present. Vanilla, Coconut and a definite sherry influence is noticeable. Jam, condensed fruit perhaps like a Plum, Blackberry or Boysenberry jam. Cinnamon and a woft of peat and smoke is very present, I would say more smoke than peat. What I am loving about this is that ‘Funk’ – Funky, Damp earthiness, Dunnage, Mossy smell. Fungal and Foosty. The more you smell the more it reveals – Which is probably some famous last words but you start to get slapped in the face with a 12 inch Salami, Meaty and Fatty. Oh yeah!", 
              "Adelphi, I can’t rave enough about them. These ‘breath of’ series are un named distilleries because they don’t want to be named. Like Voldemort, names we don’t speak of. But with a bit of googling, you can likely find out. Adelphi Breath of Isles 12yo is bottled at 58.7%, Distilled in the Isles in 2007 and bottled in 2019. This release was limited to 347 bottles.", 
              "The nose is complex and absolutely incredible. It is filled with dark notes of oiled leather, tobacco, bourbon-soaked cherries, and German chocolate cake. Even after letting it sit for a few minutes, there is still a pretty noticeable, yet not overpowering, ethanol burn on the nose. Upon a heavier nosing, notes of cherry cola and oak spice are gathered. I can already tell that the palate is going to be humongous!", 
              "Picture this: you are walking through a pine forest in the middle of autumn, eating apricots. In the distance, a grandma in a wood cabin is making a homemade cherry pie. That is exactly what this whiskey smells like. A very faint hint of green apples comes in, along with some toffee, blackcurrant and plum. The nose is deep and full of flavor, I could live inside of it.", 
              "Butterscotch, mixed berries, vanilla cream pie, marshmallow fluff, nutmeg, clove, cinnamon.  Rich and balanced with an inviting sweet and savory tinge.", 
              "The nose will entice you with a complex array of notes including cigar tobacco, espresso, smoke, char, vanilla, cherry, cinnamon, and oak.", 
              "Cognac, figs, milk chocolate, toffee, nutmeg, caramel, and a faint plastic note (not in a bad way). Plenty of oak barrel char.",
              "Dark fruits such as plums and prunes lead the way backed up by bourbon standards vanilla, caramel, brown sugar.  Very sweet on the nose but balanced out by the heat from the Proof.",
              "The nose is complex and absolutely incredible. It is filled with dark notes of oiled leather, tobacco, bourbon-soaked cherries, and German chocolate cake. Even after letting it sit for a few minutes, there is still a pretty noticeable, yet not overpowering, ethanol burn on the nose. Upon a heavier nosing, notes of cherry cola and oak spice are gathered. I can already tell that the palate is going to be humongous!", 
              "Maple syrup covered Pecan Spinwheels, banana nut muffins, nutmeg, allspice. Very sweet with an underlying spice that balances out the experience.", 
              "Cognac, figs, milk chocolate, toffee, nutmeg, caramel, and a faint plastic note (not in a bad way). Plenty of oak barrel char.",
              "The nose is dark and sumptuous. It begins with heavy notes of apricot, dark stewed berries, and figs. Upon a heavier nosing, blackberry jam (the homemade kind, not store-bought), sweet red apples, toasted chestnuts, dark grapes, and drunken blood oranges become known. You can’t nose this too hard, as the proof does come through, but only in such a way that elevates the flavors.", 
              "Tropical notes are first to jump out of the glass, such as pineapple, toasted coconut, and citrus. There’s an underlying lanolin and slight chemical quality, however, not in an off putting or offensive way. It’s weird, but I like it! Upon further nosing, brown sugar, almonds, and golden raisin notes come through as well. Wow, I could seriously nose this whiskey all day!",
              "The nose is complex and absolutely incredible. It is filled with dark notes of oiled leather, tobacco, bourbon-soaked cherries, and German chocolate cake. Even after letting it sit for a few minutes, there is still a pretty noticeable, yet not overpowering, ethanol burn on the nose. Upon a heavier nosing, notes of cherry cola and oak spice are gathered. I can already tell that the palate is going to be humongous!", 
              "Dubble Bubble gum, apricots, sultanas, and vanilla custard.", 
              "Nutmeg, buttered biscuits, lemon and orange citrus notes are immediately recognizable. The nose is quite beautiful and filled with wonderful classic bourbon notes and very little alcohol burn.",
              "Reminds me of a Mizunara cask, incense perfume and floral in nature. Jasmine, Ylang -Ylang, lemon peel, lime, citrusy and zesty. Caramel and herbal nose at the end. Earthiness and honey like nose, honey in a hot toddy – you know, Grandpa’s cough medicine. Faint hints of baby Talc hint too.",
              "The nose is pleasant with hints of red fruit, rye spice, caramel and toffee. This is one of those whiskies you don’t want to stop nosing!", 
              "Maple syrup covered Pecan Spinwheels, banana nut muffins, nutmeg, allspice. Very sweet with an underlying spice that balances out the experience.",
              "The nose is quite pleasant with thick sweet notes of vanilla, orange marmalade, oak, and orange creamsicle. This whiskey is quite aerobatic and very pleasant to smell!",
              "Butterscotch, mixed berries, vanilla cream pie, marshmallow fluff, nutmeg, clove, cinnamon.  Rich and balanced with an inviting sweet and savory tinge.",
              "The nose is dark and sumptuous. It begins with heavy notes of apricot, dark stewed berries, and figs. Upon a heavier nosing, blackberry jam (the homemade kind, not store-bought), sweet red apples, toasted chestnuts, dark grapes, and drunken blood oranges become known. You can’t nose this too hard, as the proof does come through, but only in such a way that elevates the flavors.",
              "The nose is complex and absolutely incredible. It is filled with dark notes of oiled leather, tobacco, bourbon-soaked cherries, and German chocolate cake. Even after letting it sit for a few minutes, there is still a pretty noticeable, yet not overpowering, ethanol burn on the nose. Upon a heavier nosing, notes of cherry cola and oak spice are gathered. I can already tell that the palate is going to be humongous!",
              "The nose is deep: full of red port berries, rye spice, orange spice cake, dates, cedar, and many sweet baking spices. It is very sweet in a pastry-like sense. The port barrel finish plays a massive role in the aroma of this whiskey. This is a very complex and delicious nose.",
              "Vanilla wafers, candied orange marmalade, lemon peel, green grass.", 
              "Honey and vanilla come together perfectly to give the nose a nice, beautiful aroma right off the bat. Raisins and lime balance each other out very nicely. I can tell this is going to be a sweet, yet very well balanced palate. Cinnamon notes appear at the end as a pleasant surprise.",
              "The nose is deep, dark, and beautiful. It is full of rich aromas such as dark raisins, port berries, rye spice, and dates. Other dried red-skin fruits such as plums, dried red currants, and prunes come onto the scene as well, combining for an aroma that makes you want to start sipping it immediately. Bringing the whiskey closer to your nose, as if taking a “mock-sip” helps grasp the full delightfulness of the aroma.", 
              "Allspice, nutmeg, caramel, orange zest, and apricot.  Spice notes balance out the bright fruits.",
              "Raspberries, fried cherry pie, vanilla, apricots.", 
              "Very interesting! Fruit upfront with a touch of vanilla, lemon pledge, orange custard, and lime jello. The nose is complex with a lot going on.", 
              "Nutmeg and cinnamon are first to jump out of the glass, along with a small amount of heat from the alcohol. Subtle notes of cherry, wood, candied fruit, citrus, and gumdrop nougat candy are present, but not dominant.", 
              "The nose is fairly complex, coming off with notes of orange curaçao finished creme brulee, lemon zest, peanuts, and pears. It is definitely forward on white fruits and cream!", 
              "Sweet and spicy with candy corn, vanilla, cinnamon, and allspice.", 
              "Cinnamon heavy, golden raisins, caramel, slightly doughy, toasted bread, and oak.", 
              "Strong cinnamon leads the way with the maple syrup layered below creating a pleasant sweet and savory experience. The candied plum from the nose does not show up on the palate.", 
              "Pineapple, brown sugar, baking spices, and caramel (Freshly baked pineapple upside-down cake in a glass).", 
              "Maple syrup covered Pecan Spinwheels, banana nut muffins, nutmeg, allspice. Very sweet with an underlying spice that balances out the experience.",
              "Starts very sweet with malted barley and vanilla. The rye spice shows up again as fresh wintergreen and spearmint (gum, candy, maybe somewhat like Listerine).", 
              "Red Licorice, sweet orange oil, dusty straw, candied apple, baking spices. A nice ethanol bite letting you know it’s 55% ABV.", 
              "The nose is relatively sweet and herbal. There is obvious rye spice, dried herbs, some soft ginger, a healthy dose of vanilla, dried cherry, and a touch of oak", 
              "The nose was complex and released many notes as the whiskey rested in the glass. The initial nose was sweet and spicy. Notes of corn, malted barley, and black pepper were present. After 10 minutes in the glass, cinnamon, clove, and allspice notes were present.", 
              "The nose has notes of dark cherry, cinnamon, caramel, and vanilla to go along with the earthy and floral undertones.", 
              "Cherry flavored cigarette, chocolate/cherry cordial, cedar, and backing spices.  It comes off a little hot considering the proof and age.",
              "Caramel notes are first to jump out of the glass, followed by citrus aromas. As the alcohol burns off, the scent of port and rolo candies come through. For the proof, the nose is inviting and doesn’t reveal the fact that this is a cask strength whiskey.",
              "Initial hints of pine, orange, citrus and orange marmalade, followed by more subtle yeasty bread and cinnamon buns components. The 130.9 proof is evident, with an intense amount of alcohol hitting the nose. If left to sit and open up a bit, hints of butterscotch and raisins come through.", 
              "The nose has floral notes of lovely flowers, dark cherry, pear, caramel, vanilla, and cinnamon.", 
              "Cinnamon and vanilla are dominant with a bit of almond butter.  After a few minutes in the glass a buttered corn on the cob makes a pleasant appearance.", 
              "An absolute caramel bomb…strong caramel backed up by vanilla, golden delicious apple, clove, nutmeg (very inviting)", 
              "The nose is dark and sumptuous. It begins with heavy notes of apricot, dark stewed berries, and figs. Upon a heavier nosing, blackberry jam (the homemade kind, not store-bought), sweet red apples, toasted chestnuts, dark grapes, and drunken blood oranges become known. You can’t nose this too hard, as the proof does come through, but only in such a way that elevates the flavors.", 
              "Berry and nut trail mix…a nice balance of the Beam nutty characteristic and stone fruit from the barrel finishing.", 
              "Light and sweet with honey, vanilla, stewed pears, and nectarine.  There is a small but noticeable hint of oak.", 
              "Savory charred oak, vanilla, clove, nutmeg, and burnt brown sugar.", 
              "Cinnamon heavy, golden raisins, caramel, slightly doughy, toasted bread, and oak.", 
              "Floral potpourri, clove, allspice, lemon peel, and freshly cut hay. Very spicy and floral without much sweetness. ", 
              "Sweet French Burnt Peanuts (the snack food), slightly medicinal Fred Flintstone Vitamin note.  This nose is a head scratcher, and a little too sweet for my liking.", 
              "The nose is full of dynamic notes. Heavy on the toasted oak with vanilla coming through. There are hints of tobacco and toasted cedar on the back of the nose. The longer the pour opened up the more a campfire note came through.", 
              "Pleasant but straight forward nose that comes off ethanol heavy with roasted cashews, tobacco, vanilla, maple syrup, and cedar.", 
              "As you approach the glass, notes of vanilla, caramel, butterscotch, orange, and a little bit of oak enter the scene. The vanilla and caramel are prevalent right away as the nose is sweet but not overly sweet. The notes of orange and fresh fruit follow and really adds some nice balance. Then at the end, a little touch of oak comes and rounds out the nose adding even more balance. I was wondering if an overpowering corn note would come through, but I really didn’t get a corn or grain note at all.", 
              "Intensely Hoppy, with a little familiar malt peeking through.  The nose is a little one dimensional to me but that may be the fact that this is far outside of my wheelhouse flavor profile.", 
              "Stewed apples and pears. Caramel, nutmeg, cinnamon.", 
              "Tropical Punch-mango, pineapple, strawberry, raspberry.  Under the fruit I get a sweet and spicy note reminiscent of gingerbread cookies with shortening.  Overall a great mix of aromas.", 
              "Light with traces of peaches, apricot and brown sugar.", 
              "Brazil nuts, cherry cough syrup, toffee, and nutmeg. ", 
              "The nose is light and pleasant, with hints of peanuts, honey, vanilla, and toffee. More subtle scents of baking spice and gingerbread are present as well.", 
              "Heavy dried fruits, refreshing citrus and ethanol notes hit the nose first. After opening up a bit finer notes of honey, vanilla, and a touch of oak come out.", 
              "Banana and a nuttyness are the first notes to jump out of the glass, followed by sweet corn, oak, vanilla, and white skinned fruits. Very much a classic Heaven Hill nose.", 
              "The nose was astringent with subtle hints of caramel, butterscotch, maple, and burnt char.", 
              "The nose is complex with sweet rye spices, toasted oak, and smoke. Toasted marshmallow and hazelnut begin to appear as the spirit opens in the glass.", 
              "Medley of berries…raspberry, blueberry, and blackberry.  Almond butter and hazelnut.", 
              "Cherry Cordials, vanilla, cinnamon, fried apples, and slight astringent oak.  There is also a floral aroma lurking in the background.  The nose is in line with what I consider the “Modern Turkey” profile.", 
              "Classic high age MGP nose of salted caramel, green apple, orange, and a slight dill.", 
              "Bananas Foster, nutmeg, cinnamon, dusty corn, black pepper.  I wish the banana note was a little more integrated with the other notes.  ", 
              "A unique amalgamation of Juicy Fruit gum, Mint Chiclets, and citrus peel.", 
              "Dusty straw, eucalyptus, citrus peel, and fresh cut grass.", 
              "Ethanol forward but with an underlying sweetness of black cherry cola, caramel, vanilla, and a hint of butterscotch", 
              "A pleasant aroma of light maple syrup is at the forefront of the nose. Backing it up are scents of white corn, dill, and rye spice. Touches of white fruit come in at the end to tie everything up. The nose is fairly complex considering its age, and it very pleasing.", 
              "Spicier than I was expecting with the BT mash bill #1.  Cinnamon, clove, nutmeg, and allspice. The sweetness comes across as caramel.", 
              "Crisp citrus zest, honey, cordial cherry, and cedar. Subtle, clean, and balanced.", 
              "Lightly sweetened fruit hits the nose first followed by full floral notes. There are hints of vanilla, oak, and caramel.", 
              "The nose on this bourbon was its best quality in my opinion and started off with notes of corn, vanilla, butterscotch, peach, and orange. The sweet notes of vanilla and butterscotch really shine as they rise up out of the glass. The scents of fresh fruits go nicely with the sweetness making for a very pleasant aroma. With the product being 99% corn, I was worried how much the corn note would come through, but it simply wasn’t a problem.", 
              "Hot with vanilla and a funky sour grape that threw me off when first nosed, interesting but not in my wheelhouse. ", 
              "Cask finishing dominates…fermented grapes, dark chocolate, stewed pears.  More familiar bourbon notes of caramel, almonds, and a little clove can be found beneath the other aromas.", 
              "The nose on this whiskey is one of its best attributes, with honeycomb, candle wax, and citronella dominating. Faint hints of spearmint exist, along with typical rye whiskey notes. Despite the rum soaked oak Spire, any hints of rum on the nose are subtle at most.", 
              "Key lime, citrus, margarita, and buttery syrup.", 
              "Immediate Strawberry licorice, caramel, and white pepper.  More like a high rye bourbon than a rye whiskey with the sweetness and a little light given the proof.", 
              "Fruit heavy with golden raisins, peaches, apples, and honeydew.  Underlying honey and vanilla with caramel showing up after several minutes in the glass.", 
              "Buttered Rye toast, baked graham cracker pie crust, cinnamon, honey, and orange peel", 
              "The nose starts off with flavors of sweet vanilla and bubblegum with accents of corn and allspice throughout. The most prominent note being bubblegum which really ties in nicely with the little bit of spice that is present.", 
              "Right from the beginning, corn and cinnamon come forward. The nose is not overpowering but quite pleasant especially as sweeter notes of butter, movie popcorn, and green apple enter the scene. As the whiskey opens up, notes of cinnamon start to fade away as the buttery notes become more prominent.", 
              "Spirit driven, light and fruity…pear, tangerine, pineapple, lemon grass, and slight vanilla", 
              "Light with traces of peaches, apricot and brown sugar.", 
              "Heat is the first thing to jump out of the glass, followed by intense green hay notes. Other scents identified were mint, parsley, and green wood.", 
              "Initially, a pungent ethanol note and a hint of textile rubber dominated the nose once this bourbon was in the glass. However, with some patience and time a more rich profile developed and tapered the ethanol, revealing smoky oak char, toffee, cinnamon, and a strong note of vanilla buttercream.", 
              "Banana runts candy, tropical punch, honey, and lemon grass. Bright and fruity with just a hint of youth showing.", 
              "The whiskies aromas are almost completely covered by the Port finishing. Dusty raisins, fermented grapes, and a light maple syrup shows up after several minutes in the glass.", 
              "The nose is heavy of corn bread and raisins. Notes of mandarin orange, vanilla, and lemon are slightly present at the backend of the nose. There are youthful qualities on the nose as well with a slight alcohol burn.", 
              "Sweet buttered corn, craisins, and sour grapes.  There is a sharpness that isn’t ethanol, which I can deal with, that isn’t very pleasant.", 
              "Unripe banana, pear, vanilla, and honey sweet cornbread.  Sweet and inviting with just a very slight sting when you really get down into the glass.", 
              "Toffee, golden raisins, plums, and quite a bit astringent.", 
              "The nose is fairly complex, coming off with notes of orange curaçao finished creme brûlée, lemon zest, peanuts, and pears. It is definitely forward on white fruits and cream!", 
              "The nose is sweet with banana notes wafting from the glass. Vanilla, oak, corn, and alcohol are also present.", 
              "Surprising more aromatic than I anticipated for the Proof and age. It is corn forward with peach, apricot, and honey undertones.", 
              "Earthy red clay, rose water, and ginger.", 
              "The nose starts off with spices, heavy oaky notes, and a bit of creamy caramel. Notes cinnamon raisin bread and ethanol were present as well.", 
              "The nose is somewhat off putting as the main note is the scent of hay that you might smell at a farm. There are also notes of corn and wheat that don’t really add much to the flavor profile."]

newPalateCol = ["Burnt oak and caramel are the first two things that immediately take over the palate. The burnt oak is one of the most pleasing flavors I’ve ever had in a rye; it really showcases where it came from and how it was aged. The sweetness of the caramel pairs with an incredibly thick mouthfeel with an oily texture. As the flavor moves to the mid-palate, that bright orange flavor takes over both on the sides of the tongue and the cheeks, making for a delicious sip. The back of the palate feels heavily the spice of the rye as well as the burnt oak.",
                "Oh My – Oh My – I think I am getting a bit overexcited. Funky, flinty and it is a dirty dirty whisky! So dirty, like Prince Andrew Dirty (too soon?) Robust flavour profile and very complex, There is a lot going on there. Spice, candied ginger, Fruitcake with cinnamon and some chalkiness with a hint of bitterness at the end of the palate. Smoke wofts through the back of the palate, The spirit permeates into a mouthful. Chewy and full, great mouthfeel. With Water: The smokiness comes through more, A bit sweeter with water. Bitterness at the end subsides, Funkiness is more pronounced which is great. The flavour does not change too much just slight variation.",
                "Sweet meat, Bizarre and strange – smoky, peaty, oily. A little strange but not in a bad way. The smoke and earthiness and salinity is a theme. There is a bourbon influence in there, I am sure it is an ex bourbon cask. Coconut, vanillin but what surprises me is a classic cold fermented Italian salami. Pork, pig fat, hint of smoke, black pepper. There is a slight fruitiness in there, though it is not fruity in general but a slight jackfruit hint. With water: Changes dramatically. Iron, metal, hefty and heavy. herbal, fresh chopped oregano. Unmistakable pine resin is there, fruit subsides and getting cinnamon quills.",
                "The palate is equally as impressive as the nose. The palate is thick, and contains amazing amounts of flavor. I immediately have the entire palate coated by dark chocolate cake, wet leather, dark tobacco, oak spice, cocktail cherries, and cherry cola. The flavors are extremely robust, pushed forward by the intense proof. It leaves absolutely nothing to be desired, cowering every single aspect of what a bourbon should.",
                "The palate is thick and oily. Apricot, oak spice and something like fried dough are at the front of the palate. Dark cherries (kind of like that cherry pie taste), toffee, and dates come in for an incredibly dark, fruity mid and back palate experience. The flavors coat the entire palate and hang onto it tightly. A very slight hint of chocolate comes in at the end of the palate, making it very well rounded, deep, and complex.",
                "Heavy cola at the front of the palate then transitions to butterscotch, vanilla, and brown sugar.  The spices from the nose are present along with a dash of cornmeal.",
                "The first sip coats the mouth and has a medium viscosity. Notes of char, tobacco, caramel, and vanilla are present. The second sip erupts with toffee, smoke, and dark chocolate notes. The spirit warms the mouth and settles with a heat in the chest. This third sip is an incredible mixture of all the tasting notes listed above and permeates the entire mouth.",
                "Cinnamon, orange liqueur, figs, cognac, molasses, and maple syrup. A very complex and balanced palate with a beautiful mouthfeel.",
                "A burst of flavor; thick with blueberry maple syrup, fruit punch, brown sugar, and vanilla soufflé.  There is a little heat present but nothing excessive given the high ABV.",
                "The palate is equally as impressive as the nose. The palate is thick, and contains amazing amounts of flavor. I immediately have the entire palate coated by dark chocolate cake, wet leather, dark tobacco, oak spice, cocktail cherries, and cherry cola. The flavors are extremely robust, pushed forward by the intense proof. It leaves absolutely nothing to be desired, cowering every single aspect of what a bourbon should.",
                "The scents from the nose transition to the palate intact with the spices coming forward a little stronger than they did on the nose. I must admit that I was expecting a little more viscosity on the palate for a 14yr old, but it is by no means thin.",
                "Cinnamon, orange liqueur, figs, cognac, molasses, and maple syrup. A very complex and balanced palate with a beautiful mouthfeel.",
                "The palate is medium-heavy bodied, with a bit of a syrupy consistency. It bursts with notes of dark stewed berries, cinnamon, blackberry jam, and dark imported figs on the mid palate. On the mid-back palate, dark grapes, oak spice, honey, and grape leaves.The front palate has a slight tingle of honey and oak spice that remains there throughout the duration of the sip. This is a very well put-together palate; all of the flavors cling on as soon as you take a sip and refuse to leave well after the whiskey is swallowed.",
                "The palate on this whiskey is thick, buttery, and downright tasty. Brown sugar notes are right up front, followed by orange, lemon, and a hint of cherry. As the palate begins to fade, delicious butterscotch flavors make an appearance.  Yum!",
                "The palate is equally as impressive as the nose. The palate is thick, and contains amazing amounts of flavor. I immediately have the entire palate coated by dark chocolate cake, wet leather, dark tobacco, oak spice, cocktail cherries, and cherry cola. The flavors are extremely robust, pushed forward by the intense proof. It leaves absolutely nothing to be desired, cowering every single aspect of what a bourbon should.",
                "Starts with strawberry Twizzlers, banana cream pie, nutmeg.  It then transitions away from the fruits to chocolate, burnt sugar, and a little graininess (which comes together to create a s’mores quality).",
                "Burnt maple, candied cherries, chocolate, caramel, toasted cinnamon, toffee, and vanilla. Wonderful sweet qualities that are accompanied by very enjoyable burnt/charred flavor that reminds me of the toasted sugar on the top of Crème brûlée.",
                "The ABV of this will definitely singe the hair off your face! But in a good way. Passionfruit, lemon peel, lime rind, Pineapple. Toffee and honey. Slight spice – finding it hard to describe the spice but it is more heat like candied ginger. Resin of pine needles and not so much earthiness on the palate. Vanilla, coconut essence. With Water: Eases the heat, flavor is more palatable and more approachable. The flavors are really the same but they are tapered back and able to be accepted by the mind a bit more – instead of a mind boggling flavor sensation. Slight smokiness and earthiness with water.",
                "Rye spice initially coats the mouth followed by fruity notes, and creamy orange citrus flavors. The mouthfeel is very enjoyable with just the right amount of viscosity.",
                "The scents from the nose transition to the palate intact with the spices coming forward a little stronger than they did on the nose. I must admit that I was expecting a little more viscosity on the palate for a 14yr old, but it is by no means thin.",
                "This whiskey has a very thick mouthfeel that coats the entire mouth, and it’s delightful. Flavors of dried and candied fruit, brown sugar, oak, clove, and vanilla dominate. There is a pleasant prickle from the 59.15% ABV, which is quite pleasant.",
                "Heavy cola at the front of the palate then transitions to butterscotch, vanilla, and brown sugar.  The spices from the nose are present along with a dash of cornmeal.",
                "The palate is medium-heavy bodied, with a bit of a syrupy consistency. It bursts with notes of dark stewed berries, cinnamon, blackberry jam, and dark imported figs on the mid palate. On the mid-back palate, dark grapes, oak spice, honey, and grape leaves.The front palate has a slight tingle of honey and oak spice that remains there throughout the duration of the sip. This is a very well put-together palate; all of the flavors cling on as soon as you take a sip and refuse to leave well after the whiskey is swallowed.",
                "The palate is equally as impressive as the nose. The palate is thick, and contains amazing amounts of flavor. I immediately have the entire palate coated by dark chocolate cake, wet leather, dark tobacco, oak spice, cocktail cherries, and cherry cola. The flavors are extremely robust, pushed forward by the intense proof. It leaves absolutely nothing to be desired, cowering every single aspect of what a bourbon should.",
                "The palate is medium-thick bodied. The very first thing I noticed was the presence of the port. Dark red port berries cover the mid-palate and cling on for dear life. Black cherries, figs, and blackberries stick to both the mid palate as well as the sides of the palate. The front of the palate is tingled by a heavy rye/oak spice that punches through the sweetness of the port. Small notes of ginger and orange peel are also present on the sides of the back palate.",
                "Loads of spice, cinnamon red hots, orange jelly beans, lime, and citrus.",
                "The mouthfeel is silky and fairly thick. This definitely feels hotter than its proof, in a good way. Immediately I can tell how sweet this whisky is, it is definitely a dessert scotch. Big, bold flavors of honey burst on the front and middle of the palate. Caramel, gingerbread, raisins and creme all come together on the middle of the palate beautifully, while orange zest plays on the roof of the mouth. The back of the palate receives heavy notes of something like toasted, cinnamon sugar covered almonds. I could drink this all day, it is beautiful.",
                "The body is thick, viscous, and rich. A lot of this is due to the port wine that was blended into the whiskey. Notes of dried red currants, raisins, rye spice, and dark berries coat the mid and back palate. The rye spice plays gently on the front of the palate, while the darker flavors concentrate more on the back. Dried red fruits as well as a very slight breadiness, almost like the after-taste of a strawberry grain bar are present on the mid palate as well. This is something I could drink a lot of.",
                "Spicy oak (allspice, nutmeg, and cinnamon), milk chocolate, vanilla, and burnt sugar.",
                "Cherry syrup (pie filling), pecan pie, butterscotch, baking spices, and vanilla.",
                "Intense. Layers of orange, caramel cream, and oak. The mouthfeel is wonderful and quite viscous. More subtle notes of dried cherries and raisins.",
                "Creamy with flavors of nutmeg, allspice, egg custard, orange marmalade, and pumpkin pie. Classic bourbon notes are present as well, such as vanilla and caramel.",
                "The palate is thin-medium in viscosity. I get strong notes of roasted peanuts, honey, eucalyptus, oak, pear skin, and orange. These notes cover the entire palate, and are pretty complex. This is delightful!",
                "Oily texture and a brown sugar bomb with buttered popcorn, whipped cream, and cinnamon.",
                "Orange peel, raisins, toffee, buttered popcorn, allspice, cinnamon, vanilla cream pie, and apricots.",
                "Strong cinnamon leads the way with the maple syrup layered below creating a pleasant sweet and savory experience. The candied plum from the nose does not show up on the palate.",
                "Buttered popcorn, pie crust, and tropical fruits (pineapple, coconut, kiwi, and passion fruit).  Fleeting hints of charred butterscotch.",
                "The scents from the nose transition to the palate intact with the spices coming forward a little stronger than they did on the nose. I must admit that I was expecting a little more viscosity on the palate for a 14yr old, but it is by no means thin.",
                "Starts very sweet with malted barley and vanilla. The rye spice shows up again as fresh wintergreen and spearmint (gum, candy, maybe somewhat like Listerine).",
                "There is a lot going on here with orange soda (even with an effervescent sensation on the front of the tongue), allspice, ginger, clove, vanilla, sorghum syrup, and just a hint of dill on the tail end.",
                "This whiskey delivers a quick burst of peppery rye spice up front, along with the slightest touch of alcohol burn. This is accentuated by nice spice profile, consisting mainly of allspice, cinnamon, and anise. The spices are quickly balanced by some sweet bubble gum notes, plenty of dried cherry, and dried citrus peel.",
                "The first sip was pleasantly spicy. The top of the tongue was coated with rye-spice heat with a myriad of flavors concentrated in the back palate. The second sip revealed a medium bodied viscosity that coated the entire mouth with the same punch of the first sip. Several flavors emerged including the sweetness of malted barley, corn, honey, dried fruit, and black pepper. The third sip progressed to notes of honey, tree nuts, and toasted marshmallows.",
                "The palate is very refreshing with notes of caramel, cherry, and a mild cinnamon to go along with the earthy and floral undertones. The bourbon is fairly complex with its combination of sweet and earthy flavors and has a nice finish for only being 90 proof. It has a medium viscosity and coats the entire palate. When water is added the flavors hold up great. This would be superb for a cocktail.",
                "Thinner viscosity than anticipated. Still getting the cherry cordial.  Caramel joins the party with a minty undertone.",
                "The proof is more present on the palate, although not overwhelming. Rye spice jumps out, along with sweet orange and pipe tobacco notes. The palate is oily and coats the mouth well. ",
                "This whiskey is barrel strength and it lets you know it! The heat from the alcohol is initially somewhat overwhelming and mutes many of the flavors. As the palate gets acclimated, the classic Blanton’s cinnamon notes come through, along with hints of the retro Slo Poke candy. A few drops of water does this whiskey well, releasing flavors of honey butter, chocolate and coffee.",
                "The palate is excellent with notes of caramel, toffee, pear, apple, dark cherry, vanilla, and cinnamon. All of the flavors are very developed and distinct. The bourbon has a medium viscosity and coats the entire palate before dissipating. When you add water, the flavors hold up. This pour would be absolutely fantastic in an Old Fashioned or Manhattan as the bourbon flavors would shine through.",
                "Spicy with cinnamon and nutmeg.  The sweetness comes in the form of Bananas Foster and brown sugar.  The little heat on the tongue works in concert with the flavors for an enjoyable and classic bourbon experience.",
                "Not as rich as the nose suggests but many of the same notes are present with caramel at the forefront, apple peels, and baking spices. Then an interesting hoppy bitterness shows up on the tail end.",
                "The palate is medium-heavy bodied, with a bit of a syrupy consistency. It bursts with notes of dark stewed berries, cinnamon, blackberry jam, and dark imported figs on the mid palate. On the mid-back palate, dark grapes, oak spice, honey, and grape leaves.The front palate has a slight tingle of honey and oak spice that remains there throughout the duration of the sip. This is a very well put-together palate; all of the flavors cling on as soon as you take a sip and refuse to leave well after the whiskey is swallowed.",
                "It is usually on the palate that sherry/wine finished bourbons fall off for me with too much of a fermented grape characteristic (I’m not a wine drinker) but here the balance from the nose continues with the intrinsically nutty Beam playing nice with the Stone fruits. The finishing creates a nice viscosity that is hard to achieve with what is a fairly young bourbon.",
                "Honey drizzled over fresh fruit with vanilla and caramel undertones. Very sweet with little to no heat.",
                "There is an initial caramel/vanilla sweetness and then the spice cabinet opens with a dash of black pepper, cinnamon, nutmeg, allspice, and clove.",
                "Orange peel, raisins, toffee, buttered popcorn, allspice, cinnamon, vanilla cream pie, and apricots.",
                "Starts out with a small amount of cordial cherry sweetness that quickly transitions to citrus, allspice, clove, cinnamon, and cardamom.  More heat than I initially expected.  ",
                "Thankfully much spicier than the nose leads to believe with nutmeg, allspice, and anise.  The French Burnt Peanuts are still present but as prevalent as on the nose with a hint of pie crust.",
                "This whiskey had many layers of flavor. First, the palate was hit with warm vanilla, allspice, honey, and a hint of heat. As the whiskey sat in my mouth, the flavors shifted to a coconut, caramel, and toasted cedar. Each sip of this bourbon was very coating from a nice viscosity. The longer I let the pour breathe, the more of the malted beer notes came through on the palate. The complexity of the flavors leaves you longing for another sip.",
                "There is an interesting ethanol singe on the front of the tongue that some may find off-putting followed by sweet pecan pie, vanilla, nutmeg, and cardamom.",
                "As the bourbon enters you mouth, it moves from the front palate to the back palate in a very rhythmic fashion. On the front palate, notes of caramel, peanuts, and baking spice really shine through. Then as the bourbon coats the mouth and moves to the back palate, a slight char becomes apparent and causes a smooth burn that really adds to the aromatic properties of the bourbon. The mouthfeel is a medium viscosity, and the bourbon coats the palate nicely.",
                "Hops continue to lead the way but with a little more complex flavors beginning to show up from the barrel (honey, vanilla, and smoke).",
                "A surprising amount of butterscotch is noticeable with an unsurprising amount of baked apple pie.",
                "The fruits from the nose are all present here but they are not as intense as I was expecting.  Spices such as nutmeg, ginger, clove, and just a hint of white pepper are more prevalent than the nose would have you believe. The bump in Proof is noticeable but overall a subtle palate.",
                "Sweet notes of brown sugar, caramel, cherries, and baking spice spices (nutmeg, cinnamon and clove). The flavors are nicely balanced.  ",
                "Chocolate covered almonds, cold medicine, and the familiar but faint Flintstone’s Vitamin.",
                "The nutty flavors from the nose carry right over to the palate, along with the toffee, vanilla, and gingerbread. There is very little body to the palate and is distinctively thin and non-viscous.",
                "Peppery wood notes are first to hit the palate, quickly followed by creamy vanilla that coats the entire palate. Lastly, crisp citrus and sweetness of dried fruits hit the back of the palate.",
                "The nutty notes from the nose carry through to the palate, along with an almost salt like quality. Salted peanuts? Sure! Plenty of caramel and corn characteristics are present as well.",
                "The first sip was astringent and punchy with a faint taste of tree nuts. The second sip had the same astringency, however, some char and smoke notes shone through. The third sip had faint notes of butterscotch and tree nuts. After 10 minutes, the next sip revealed vanilla, cinnamon, and faint barrel char.",
                "The first sip has a silky mouthfeel. There is some heat concentrated in the back palate that flows into the chest. Smoke notes are present. The second sip has a medium viscosity. The flavors envelop the entire mouth. Sweet rye spice, toasted oak, and smoke are most prominent. The third sip consists of smoked vanilla and toasted marshmallows.",
                "A sticky caramel sweetness dominates with an underlying oaky vanilla.  Just the slightest of baking spices nutmeg and ginger appear under an overarching minerality. ",
                "Brown sugar, vanilla, crisp apple, orange zest, nutmeg, cinnamon, and charred oak.  The rye spice makes its presence known.",
                "Follows the nose closely with strong caramel with the spicy notes laying a nice foundation, unfortunately a little thin.",
                "Bananas Foster is at the front of the palate but less prominent than on the nose.  Pecan Spinwheels heavy with baking spices follow.  Nice confectionary sweetness balanced by spice.  ",
                "Red Hots, peppermint, toffee, caramel, allspice, and clove.",
                "Sweet citrus leads the way, with the herbal eucalyptus and vanilla following.",
                "Wood varnish and allspice take the place of the sweetness of the nose. While spice forward touches of vanilla wave in and out of the palate.",
                "Light maple syrup and vanilla give the front of a nice, sweet sensation. The mouthfeel is thicker than what one would expect from a 92 proof whiskey, likely due to the non-chill filtration. On the mid-palate, juniper berries, pine needles, and black pepper appear in a very pleasant manner. It makes me feel like I should be drinking it in front of a fire and a fresh Christmas tree.",
                "Pie crust, nutmeg, vanilla, and confectionery sweetness similar to cotton candy.",
                "Surprisingly oily given the proof.  Sweet…honey drizzled biscuits, maple syrup, and pipe tobacco. Sweetness offset with a dash of white pepper.",
                "The palate is fairly smooth and there is not much spice on the first sip but that does not discount the flavor. The second sip coats the mouth with notes of raisins, vanilla, and almonds. There are also floral notes followed by rich dried fruit notes.",
                "As the bourbon enters your mouth, it jumps straight to the back palate, but as the flavors develop, a very refreshing note appears on the front palate. The main notes that showed up on the palate were a sweetness that was mostly driven by vanilla as well as a light spice that was led by allspice and a nice full-bodied cinnamon.",
                "The funky sour notes are thankfully absent from the palate where the vanilla begins to dominate with just a touch of cocoa underneath. ",
                "I get an initial flash of the higher rye bourbons from MGP that many know and love…caramel, vanilla, and nutmeg. Unfortunately, that is quickly replaced with (in my opinion) a rather heavy-handed finishing.  The fermented grapes return with the dark chocolate and sour raisins.",
                "Heavy amounts of green tea, much like citrus Lipton Green Tea. Rye flavors coat the mouth well with just a hint of spice from the 95% rye mashbill. The palate on this is creamy and sweet, much like an over sweetened herbal tea.",
                "The key lime qualities from the nose do not follow through to the palate, however there are still some citrus characteristics in the form of orange marmalade and orange peels. The texture on the tongue has a waxy/paraffin component that coats the mouth. There’s an abundant amount of sweetness and texture with this bourbon that is reminiscent of eating pure honeycomb. Lastly, brown sugar and butterscotch notes exist, reminding us of the syrup you’d get on an ice cream sundae.",
                "Oh, now I see it’s a rye!  Allspice, cardamom, and star anise dominate with just enough toffee sweetness to balance the spice.  ",
                "I get the honeydew from the nose up front with milk chocolate and baking spices coming in as the whiskey saturates the palate.",
                "The palate is dominated by baking spices with just enough vanilla and caramel to help balance out the spice level.  A dash of black pepper on the back of the palate.",
                "The palate is sweet with notes of hard candy and bubblegum. The little bit of spice from the nose carries over and provides balance to the sweetness of this whiskey. Overall, I was pleased with how the bubblegum of the nose carried over to the palate.",
                "As the whiskey enters, you immediately get notes of cinnamon and allspice which are followed by some vanilla and even a hint of leather. I found the palate to be sweet which was quite pleasant as it matched up with the nose. ",
                "Spirit driven, light and fruity…pear, tangerine, pineapple, lemon grass, and slight vanilla",
                "Sweet notes of brown sugar, caramel, cherries, and baking spice spices (nutmeg, cinnamon and clove). The flavors are nicely balanced.  ",
                "Mint notes up front, followed by a rush of cinnamon and alcohol burn. Fruity and confectioners sugar come up on the mid palate but are quickly stripped away by an intense drying effect.",
                "On the palate, the alcohol created a fairly strong burn up front (this is a barrel proof bourbon after all), but not so much as to completely overpower the other flavors that developed throughout the sip. The mouthfeel was average and I found a dominant note of burnt sugar, heavy corn, more of that smoky oak char, and a fairly sharp rye spice that developed on the back of the tongue.",
                "Thin with the tart fruit from the nose being the dominant factor. There is not much depth to here unfortunately.",
                "Just like on the nose, the Port dominants the taste, which some may really like. Unfortunately it’s just not in my wheelhouse. ",
                "The body is light. The palate is very forward with a note of buttery toffee banana, and citrus, mainly orange. Some vanilla creeps in, but is not overly present. It is very yeasty as well. The palate overall is not very complex nor deep, even for the proof.",
                "Thin viscosity with bitter fruit up front followed by youthful grain notes.",
                "The fruits from the nose hit the front of the palate as Golden Delicious Apples.  Some pear remains but the prevalent banana from the nose is absent.  Caramel and vanilla then take over creating a pleasurable but not too complex of a flavor profile.",
                "Thin with dark fruit, nutmeg, and a slight hint of allspice.",
                "The palate is thin-medium in viscosity. I get strong notes of roasted peanuts, honey, eucalyptus, oak, pear skin, and orange. These notes cover the entire palate, and are pretty complex. This is delightful!",
                "The first sip is thin, producing a tingle on the front and sides of the tongue. Slight effervescence is accompanied by sour wood and faint char. The second sip reveals pronounced notes of corn, and banana. Faint grass notes were present on the third sip.",
                "Corn forward again with a slight hint of the fruit from the nose. Nothing too special here but also nothing off-putting per-say.",
                "Very thin with ginger bread cookies, melon, and green apples.",
                "Toasted oak is the first major note. Soon followed by toffee, butterscotch, vanilla, and cinnamon spice. The overall viscosity of the bourbon was thin on the palate.",
                "As the whiskey enters the palate, notes of hay and corn make up most of the mouthfeel. There is also an unpleasant burn that is present from front palate all the way to back palate. This whiskey leaves a lingering aftertaste that I wasn’t fond of personally.",]

newFinishCol = ["The progression of the finish is nearly the same as the palate. It starts with that big, beautiful barrel char and then leaves an incredibly long, sumptuous orange-rind linger that sticks to the tongue for what seems like forever.",
                "Not as long and oily as other Longrows but a very complex dram, medium to long finish. With water the finish becomes longer.",
                "Holy crikey! This is a busty, ballsy, arnie ‘ballsy’ dram. Oily beast, sweet hit and savory follow up. This is not for the faint hearted, this is not smooth – this is intriguing and compelling but ‘not smooth’ Uber complex. Salty, oily, resin, smoky, enveloping flavors and crazy intensity. Right now, I am getting a massive flavor bomb, hard to break down the small flavors but what I am getting is pig, pork, pork crackling, salami, pork fat. The sweetness, is a caramel sugar then quick to be followed by pork fat! With water: Tapers back the alcohol – first impressions, hard to tell which is better, mouthfeel changes, less viscous, less intense, much more palatable but flavors are similar, intensity just tames down – but it is still a beast. Just think Mike Tyson in the 90s vs his come back. He is still an animal, I wouldn’t want to mess with him but certainly tamed over time. Burnt brown sugar, oily, peaty comes through more. Smoke lingers.",
                "The finish is very long, and carries over just about every flavor that the palate contained. The flavors stick to every single aspect of the palate, including the roof of the mouth. I can wait several minutes in between sips and be perfect satisfied. I believe that the lack of chill filtration assists in this greatly, and I am glad that Heaven Hill has continued to do this with the new releases.",
                "The finish is long and deep. Flavors of cherry, pie crust, plums, and oak spice cover every single part of the palate. It just keeps rolling into more flavors like milk chocolate and apricot at the end of the finish. You can take several minutes in-between sips and be fully satisfied.",
                "Roasted almonds and marshmallows.  Spices swell in the chest with a pleasant warming sensation.",
                "The finish is long and pleasant. The heat from this bourbon is evident across the top of the tongue and stimulated a Pavlovian response. Notes of smoke, oak, and char are initially present. These favors progress into cinnamon and dark roast coffee. As the bourbon lingers faint notes of cinnamon and clove emerge.",
                "Cocoa, cinnamon rolls, raisins, cake, and figs. This bourbon has a very long finish with many complex layers",
                "All the sweet notes continue and are joined by cinnamon and ginger.  Decent length and the heat dissipates into a subtle warmth.",
                "The finish is very long, and carries over just about every flavor that the palate contained. The flavors stick to every single aspect of the palate, including the roof of the mouth. I can wait several minutes in between sips and be perfect satisfied. I believe that the lack of chill filtration assists in this greatly, and I am glad that Heaven Hill has continued to do this with the new releases.",
                "Now that’s what I’m talking about…the 14 years in the barrel really show on the long vanilla and baking spice finish. Drying sandalwood linger for several pleasant minutes after the sip.",
                "Cocoa, cinnamon rolls, raisins, cake, and figs. This bourbon has a very long finish with many complex layers",
                "The finish is long, you can take couple of minutes between sips and not miss a thing. The dark berry and fig notes remain on the mid palate, as well as a tingle of oak spice on the mid-back palate. This is where the armagnac shines, it gives the whiskey enough viscosity to hang on to the tongue and cheeks for a long time.",
                "The finish is pleasantly long with lemon and citrus that evolves into a touch of cherry and cinnamon. The Butterscotch notes from the palate continue to linger around throughout the finish.",
                "The finish is very long, and carries over just about every flavor that the palate contained. The flavors stick to every single aspect of the palate, including the roof of the mouth. I can wait several minutes in between sips and be perfect satisfied. I believe that the lack of chill filtration assists in this greatly, and I am glad that Heaven Hill has continued to do this with the new releases.",
                "It is here that the whiskey switches it up and brings up some bitter dark chocolate, pecans, and allspice.",
                "Dark baking cocoa, orange citrus, black licorice, and a continuation of that delicious burnt sweetness from the palate. The finish is relatively long and leaves the mouth begging for another sip.",
                "Although it’s good to try this with and without water, I’d recommend always adding water with this one. The finish is big, chewy and complex.",
                "The finish is somewhere between medium and long with lots of rye spice, clove, and nutmeg. Very enjoyable! ",
                "Now that’s what I’m talking about…the 14 years in the barrel really show on the long vanilla and baking spice finish. Drying sandalwood linger for several pleasant minutes after the sip.",
                "The finish is very long-lasting with strong woody oak, vanilla, and brown sugar notes. It leaves the mouth a bit dry, but at the same time begs you to take another sip.",
                "Roasted almonds and marshmallows.  Spices swell in the chest with a pleasant warming sensation.",
                "The finish is long, you can take couple of minutes between sips and not miss a thing. The dark berry and fig notes remain on the mid palate, as well as a tingle of oak spice on the mid-back palate. This is where the armagnac shines, it gives the whiskey enough viscosity to hang on to the tongue and cheeks for a long time.",
                "The finish is very long, and carries over just about every flavor that the palate contained. The flavors stick to every single aspect of the palate, including the roof of the mouth. I can wait several minutes in between sips and be perfect satisfied. I believe that the lack of chill filtration assists in this greatly, and I am glad that Heaven Hill has continued to do this with the new releases.",
                "The finish is medium-long and is covered with spices, candied figs, oak spice, and ginger. It lingers just long enough to be satisfying but not long enough to make you feel like the flavors were sickly-sweet.",
                "Slight hints of coconut, vanilla, and butterscotch. Interesting waves of smoke and lime linger, along with a touch of licorice.",
                "The finish is medium-long and infilled with notes of honey, apple blossom, lemon, and caramel. It is an extremely tasty finish, likely prolonged due to the finishing in the Sauternes casks.",
                "The finish is long and thick. The notes of dark berries and dried, red-skinned fruit sit heavily on the mid-palate. The rye spice migrates to the back palate for the finish, but is not as noticeable as it was while I was still “chewing” the whiskey. It makes me want to keep on drinking it- a lot of it.",
                "Surprising long with the spices continuing to dominate. Oak, chocolate, and coconut (think Mounds Bar) round everything out.",
                "The sweet cherry dissipates leaving a spicy finish with cinnamon, nutmeg, allspice, and clove with an underlying oak note.",
                "The finish is long and drying. A nice creamy sweet vanilla quality lingers with plenty of oak and barrel char.",
                "This bourbon has an enjoyable finish that’s pleasantly long with flavors of cinnamon, oak and liquorice sticking around.",
                "The finish is medium-long and carries over the wonderful notes of orange, roasted peanuts, and oak.",
                "Slight tongue burn with a cinnamon swell and the other flavors from the palate linger nicely.",
                "Surprising long with musty oak, vanilla, nutmeg, cinnamon, and black licorice.",
                "Long and warm with the return of sweet tobacco and leather notes. Oak presence is noticeable but completely balanced with the other notes.",
                "Surprising long with vanilla and charred oak.  The baking spices become more defined on the finish with nutmeg, cardamom, and clove becoming more dominant.",
                "Now that’s what I’m talking about…the 14 years in the barrel really show on the long vanilla and baking spice finish. Drying sandalwood linger for several pleasant minutes after the sip.",
                "The “fresh” sensation from the palate continues and eventually fades to brown sugar.",
                "This really sticks to the cheeks.  There is more barrel influence on the finish than I noticed on the palate. The fruits dissipate leaving spice, vanilla, and caramel.",
                "The finish is medium-long with a pleasantly thick viscosity. There is some peppery rye spice and lingering heat, but the sweet notes really take over. I found more of that sweet bubble gum flavor, more dried cherry, and a touch of citrus, all underscored by soft oak notes that round out the pour.",
                "The finish was long and lingering with rye-spices and sweet malted barley. This combination was complex and enjoyable. A faint clove note became present as the finish began to fade.",
                "The finish follows the nose and palate with notes of caramel and spice as well as lingering earthy and floral notes.",
                "Tannic oak asserts itself with lingering tobacco, pine, and caramel.",
                "The finish is very pleasant and long lasting with plenty of delicious rye spice. Hints of cinnamon, orange peel, apple and vanilla stick around for quite some time. ",
                "This bourbon finished very much like the initial tasting, hot. The heat causes a good amount of drying and ultimately results on a finish that wasn’t overly long. Notes of coffee and tea seem to linger the most.",
                "The bourbon has a medium finish with the floral notes from the palate carrying through. As the bourbon finishes, there is a transition where the notes go from being more floral to sweeter notes of caramel and cherry. The bourbon has good complexity as it mingles together notes of flowers, sweetness, and spice in a balanced manner.",
                "The almonds from the nose return accompanied by milk chocolate and salted caramel.  The oak finally makes its presence known with a hint of tobacco and cedar.  A minty freshness rounds out the finish.",
                "The hoppy bitterness merges with oak tannins to create a linger finish that unfortunately falls a bit flat.",
                "The finish is long, you can take couple of minutes between sips and not miss a thing. The dark berry and fig notes remain on the mid palate, as well as a tingle of oak spice on the mid-back palate. This is where the armagnac shines, it gives the whiskey enough viscosity to hang on to the tongue and cheeks for a long time.",
                "Short with the fruity characteristics overpowering the classic bourbon notes.",
                "It is here on the finish that I figured this dram would fall off due to the proof, but I was wrong. The sweet notes linger for a few seconds before being replaced by Cinnamon Rock Candy that just sticks to all the crevasses in the mouth and refuses to go away.",
                "Medium/long length with allspice, mint tea, oak, and vanilla.",
                "Surprising long with musty oak, vanilla, nutmeg, cinnamon, and black licorice.",
                "The heat from the palate lingers for a few seconds then succumbs to an oaky toffee sweetness with a nice spice swell in the chest. ",
                "Lingering oak and vanilla balanced nicely with the spices carrying over from the palate. Medium in length.",
                "The finish hits on the back of the palate and slowly takes over the mouth, leaving along hints of the beer flavor from the soaked spire. The slight beer notes on the finish did not take away from the fact this is a whiskey but added the refreshing finish received from a beer. The beer notes on this bourbon were very enjoyable and one of my favorite qualities.",
                "Nice (slightly dry) oak presence with the return of tobacco, cinnamon, and white pepper. The ethanol heat from the nose and palate has but dissipated by this point.",
                "The bourbon has a medium finish that is led by a strong peanut note that is followed by notes of cinnamon and baking spice that begin to linger in your throat.",
                "Very long given the youth of this whiskey.  There is a surprising amount of smokiness in the finish.",
                "Short and one note given the proof with Barrel char taking the place of the apples and pears.",
                "The spices shoulder the weight of the finish with the fruits all but disappearing at this point.  A bit of Pine before fading out.",
                "Spices begin to dominate with allspice and nutmeg joining the party.  Vanilla bean also shows up.  The finish is pleasantly long and enjoyable.",
                "Charcoal joins the chocolate and almond with a lingering coffee bean.",
                "The finish is decently long, thin, and spicy. Much of the peanut nuttiness lingers around for a while too, along with a very noticeable drying effect.",
                "The finish is long and lingers for a bit of time allowing the smaller notes of oaks, toasted nuts, and light vanilla come through.",
                "The finish is long, spicy, and lingers about for quite some time. Oak dominates, with more subtle baking spices, nutmeg, and black pepper.",
                "The finish was medium and improved with time. This bourbon drank higher than 92 proof. I found it necessary to let this bourbon sit and open up in order to get many tasting notes to come through.",
                "The finish is medium to long. There is a good balance of heat and flavor. Oak spice, vanilla, dark fruit and smoke are noticeable.",
                "Despite the sticky nature of the palate the finish fades quickly with a heavy dose of mixed nuts and the continuation of the chalky minerality. ",
                "Medium in length…very spicy with leather, slight maple, and unsweetened steeped tea.  Charred oak continues throughout and is the last flavor to fade.  The #4 “alligator” char dominates the finish but in an almost artificial way.",
                "And it is here that the low proof really hurts what could have been great whiskey…the finish is almost non-existent with just a hint of vanilla, oak, and mint.",
                "Holy moly this is char heavy on the finish for the age!  Burnt brown sugar and salted caramel are fighting with ashy char for several minutes after the sip.  Warehouse location must be a major factor on what barrels go into this label because the finish is reminiscent of much older whiskey.",
                "Burst of cinnamon with vanilla laced throughout that unfortunately doesn’t last long.",
                "Herbaceous notes continue but fade safely quickly, I believe with some more age the finish can match the nose and palate.",
                "Short and tannic with not as much going on as the nose and palate.  Spices take full control of the experience.",
                "The whiskey has a medium finish which contains the sweetness from the maple syrup note and the acidity from the juniper and pine notes. They come together nicely and balance each other out. The end of the finish is very oaky.",
                "Classic bourbon profile finish of caramel, vanilla, and baking spices.  Nothing outstanding.",
                "Slightly bitter oak, brown sugar, and (strangely) watermelon rind fade quickly leaving a fresh fizzy sensation on the tongue.",
                "The finish is relatively short in comparison to other finish bourbons I have had. There is a bit of dryness from the sherry casks but a very balanced amount.",
                "The bourbon has a medium finish with a very prevalent peanut note that is accompanied by allspice and cinnamon that continues on from the palate.",
                "Oak shows up on the finish to add an extra layer of complexity to the vanilla driven experience. ",
                "It is here that the bourbon flavors finally assert themselves…vanilla, caramel, cherries, nutmeg, and oranges that linger for a few minutes.",
                "Medium in length with light rye spice and a lingering sweetness. It’s got a unique rustic quality that reminds me of being on the farm. Although the finish is nice, it’s not this whiskies best attribute.",
                "The finish on this bourbon falls into the “medium/long” category, which is impressive considering its younger age. Very rich layers of honey, brown sugar and butterscotch give way to a final hint of cotton candy.",
                "Spice prickles lingers on the tongue and the sweetness all but disappears.  Nice but simple compared to the nose and palate.  ",
                "The finish is on the shorter side with the baking spices and stewed fruit dominating.  There is a flash of oak before fading away.",
                "The black pepper from the palate lingers in the back of my throat creating a slightly unpleasant “heart burn” sensation, other than that the normal bourbon notes of vanilla, caramel, and cinnamon linger for a decent length of time.",
                "The finish is medium to long and has a burn that is full of cinnamon and allspice. A little sweetness comes from the candy and vanilla flavors that were present in the nose. The length and flavors of the finish were very pleasant.",
                "The whiskey had a medium finish with lingering allspice and cinnamon notes from the palate. The flavors carry to the finish as the allspice sits on the back palate for a fair amount of time and then slowly dissipates.",
                "Light custard, Pawpaw fruit, lemon, and pineapple. Very little oak influence.",
                "Spices begin to dominate with allspice and nutmeg joining the party.  Vanilla bean also shows up.  The finish is pleasantly long and enjoyable.",
                "Initial cranberry and strawberry notes on the finish, followed by caramel and lemon. There is a bitter and chalky quality to this whisky that’s somewhat off putting. Although there is good complexity and several different layers, the drying effect really distracts those good qualities.",
                "This bourbon has a medium finish with quite a bit of heat lingering from the proof. I also found more rye spice and burnt sugar, along with smoky oak undertones.",
                "The Barrel finally shows up in the form of vanilla and a vague burnt salted caramel.",
                "Barrel tannins and cocoa take over for a somewhat surprisingly long finish that is the highlight of the experience. ",
                "The finish is short and filled with yeast, banana, and slight citrus notes. It fades quickly and leaves you wanting more.",
                "Musty vanilla oak and char combine to create the most interesting and most pleasant part of the dram.",
                "Here is where a little of the youth shows its face, but it is not off putting.  It is on the shorter side with hints of clove and allspice coming through from the rye in the mash bill.",
                "Short and tannic with a cinnamon swell.",
                "The finish is medium-long and carries over the wonderful notes of orange, roasted peanuts, and oak.",
                "The finish is short and unpleasantly bitter. Oak and banana were the most prominent notes.",
                "Very short with just a flash of vanilla before disappearing.",
                "White pepper, clove, and honeydew fade quickly.",
                "The medium finish is crisp and refreshing. A bit of spice grabs at the end but it is not overpowering and is quickly replaced with the refreshing of the citrus found in the palate.",
                "The finish has a little bit of baking spice but mostly consists of the burn and unpleasant aftertaste that were present on the palate."]


# In[7]:


# Bind new columns together
dfTemp = pd.DataFrame(list(zip(newColorCol, newNoseCol, newPalateCol, newFinishCol)),
               columns =['Color', 'Nose', 'Palate', 'Finish'])

# Bind with dataframe to get name and url info
datRawReviewsUpdate2 = dfTemp.merge(datRawReviewsUpdate[['Name','reviewUrl']].reset_index(), left_index=True, right_index=True)

# append updated dataframe to the original dataframe that didn't have any NA's
datRawReviews3 = datRawReviews2.append(datRawReviewsUpdate2, ignore_index=True).drop(['index'], axis=1)


# In[8]:


os.getcwd()


# In[9]:


datRawReviews3.to_pickle("./whiskeyconsensus-reviews-raw-July-2021.pkl")


# In[ ]:




