
# Data
MATERIAL = {'LargeMMeshBed', 'LargePMeshBed', 'MediumPMeshBed', 'SmallPMeshBed',
            'LargeMFleeceBed', 'LargePFleeceBed', 'MediumPFleeceBed', 'SmallPFleeceBed',
        'LargeMQuiltBed', 'LargePQuiltBed', 'MediumPQuiltBed', 'SmallPQuiltBed',
            'LMFrame', 'LPFrame', 'MPFrame', 'SPFrame',
            'LFleeceTop', 'MFleeceTop', 'SFleeceTop', 'LMeshTop', 'MMeshTop', 'SMeshTop',
            'LQuiltTop', 'MQuiltTop', 'SQuiltTop', # set of products
            'Mesh', 'Fleece', 'PLegs', 'Casing', '36PRods', '30PRods', '24PRods', '18PRods', 'cash'
            'Loops', 'MLegs', 'LBox', 'SBox', '36MRods', '30MRods', 'FleeceScrap', 'Pillow', 'MeshScrap', 'Bag'}

CUSTOMER = {'Store', 'Online', 'DogShow'}
LOW_PRIORITY = {'DogShow'}     # subset oc customers, low priority
NO_LATE = {'DogShow'}          #subset of customers, can't ship late
IS_SHIPPED = {'Store'}
BUYSandSHIPS = {'Labor'}
LOCATION = {'Studio',''} #empty string represents default location
HAS_OFFSET = {'LQuiltTop', 'MQuiltTop', 'SQuiltTop'}
NEEDS_LARGE_BOX = {'LargeMMeshBed', 'LargePMeshBed', 'LargeMFleeceBed', 'LargePFleeceBed', 'LargePQuiltBed', 'LargeMQuiltBed'}
CAPACITY = {'Labor', 'LaborStudio'}
TIME = ['3-Dec', '4-Dec', '5-Dec', '6-Dec', '7-Dec', '8-Dec']

init_funds = 2000


usage = {  # list for BOM  USUAL INPUT FORMAT FROM MRP SYSTEM
    ('LargeMMeshBed', 'LMeshTop'): 1,
    ('LargeMMeshBed', 'LMFrame'): 1,
    ('LargeMMeshBed', 'Labor'): 15,

    ('LargePMeshBed', 'LMeshTop' ):  1	,
    ('LargePMeshBed', 'LPFrame' ):	1,
    ('LargePMeshBed', 'Labor' ):	12,

    ('LargeMFleeceBed', 'LFleeceTop' ):	 1	,
    ('LargeMFleeceBed', 'LMFrame' ):	1	,
    ('LargeMFleeceBed', 'Labor' ):	15	,

    ('LargePFleeceBed'   , 'LFleeceTop' ):	1	,
    ('LargePFleeceBed'   , 'LPFrame' 	):	1	,
    ('LargePFleeceBed', 'Labor' ):	12	,

    ('MediumPFleeceBed'   , 'MFleeceTop'): 	1	,
    ('MediumPFleeceBed'   , 'MPFrame' 	):	1	,
    ('MediumPFleeceBed'   , 'Labor' ):	8	,

    ('MediumPMeshBed'     , 'MMeshTop' 	) :1,
    ('MediumPMeshBed', 'MPFrame' ) :1,
    ('MediumPMeshBed'   , 'Labor' ):	8	,

    ('SmallPMeshBed', 'SMeshTop' ) :1,
    ('SmallPMeshBed', 'SPFrame' ):	1	,
    ('SmallPMeshBed', 'Labor' ):	5	,

    ('SmallPFleeceBed'    , 'SFleeceTop'): 	1	,
    ('SmallPFleeceBed'    , 'SPFrame' 	):	1	,
    ('SmallPFleeceBed', 'Labor'): 5,
#############################################
    ('LargeMQuiltBed', 'LQuiltTop'): 1,
    ('LargeMQuiltBed', 'LMFrame'): 1,
    ('LargeMQuiltBed', 'Labor'): 15,

    ('LargePQuiltBed', 'LQuiltTop'): 1,
    ('LargePQuiltBed', 'LPFrame'): 1,
    ('LargePQuiltBed', 'Labor'): 12,

    ('MediumPQuiltBed'   , 'MQuiltTop'): 	1	,
    ('MediumPQuiltBed'   , 'MPFrame' 	):	1	,
    ('MediumPQuiltBed'   , 'Labor' ):	8	,

    ('SmallPQuiltBed', 'SQuiltTop'): 1,
    ('SmallPQuiltBed', 'SPFrame'): 1,
    ('SmallPQuiltBed', 'Labor'): 5,

    ('LMeshTop', 'Mesh'	):	 36	  ,
    ('LMeshTop', 'Casing' ):	132   ,
    ('LMeshTop', 'Labor'): 	12 ,

    ('MMeshTop', 'Mesh' 	):		24 ,
    ('MMeshTop', 'Casing' 	):	108    ,
    ('MMeshTop', 'Labor'): 8,

    ('SMeshTop', 'Mesh '	):		18 ,
    ('SMeshTop', 'Casing' 	):	84     ,
    ('SMeshTop', 'Labor' ):		4,
    ('SMeshTop', 'MeshScrap'): 		-1,

    ('LFleeceTop', 'Fleece'): 36,
    ('LFleeceTop', 'Casing'): 132,
    ('LFleeceTop', 'Labor'):	25,

    ('MFleeceTop', 'Fleece'): 24,
    ('MFleeceTop', 'Casing'): 108,
    ('MFleeceTop', 'Labor'): 20,

    ('SFleeceTop', 'Fleece' ):		18    ,
    ('SFleeceTop', 'Casing' ):		84    ,
    ('SFleeceTop', 'Labor'): 15,
    ('SFleeceTop', 'FleeceScrap'): - 1,

    ('MPFrame', 'PLegs'   ): 			4 ,
    ('MPFrame', '24PRods' ):		2     ,
    ('MPFrame', '30PRods' ):		2     ,

    ('SPFrame', 'PLegs' )	:	4         ,
    ('SPFrame', '24PRods' ):		2     ,
    ('SPFrame', '18PRods' ):		2	  ,

    ('LPFrame', 'PLegs' ) :4,
    ('LPFrame', '36PRods'): 2,
    ('LPFrame', '30PRods'): 2,

    ('LMFrame', 'MLegs'): 4,
    ('LMFrame', '36MRods'): 2,
    ('LMFrame', '30MRods'): 2,

    ('Pillow', 'FleeceScrap'): 1,
    ('Pillow', 'Labor'): 3,

    ('Bag', 'MeshScrap'): 1,
    ('Bag', 'Loops'): 1,
    ('Bag', 'Labor'): 3,

('LMeshTopStudio', 'MeshStudio'	):	 36	  ,
    ('LMeshTopStudio', 'CasingStudio' ):	132   ,
    ('LMeshTopStudio', 'LaborStudio'): 	12 ,

    ('MMeshTopStudio', 'MeshStudio' 	):		24 ,
    ('MMeshTopStudio', 'CasingStudio' 	):	108    ,
    ('MMeshTopStudio', 'LaborStudio'): 8,

    ('SMeshTopStudio', 'MeshStudio '	):		18 ,
    ('SMeshTopStudio', 'CasingStudio' 	):	84     ,
    ('SMeshTopStudio', 'LaborStudio' ):		4,
    ('SMeshTopStudio', 'MeshScrapStudio'): 		-1,

    ('LFleeceTopStudio', 'FleeceStudio'): 36,
    ('LFleeceTopStudio', 'CasingStudio'): 132,
    ('LFleeceTopStudio', 'LaborStudio'):	25,

    ('MFleeceTopStudio', 'FleeceStudio'): 24,
    ('MFleeceTopStudio', 'CasingStudio'): 108,
    ('MFleeceTopStudio', 'LaborStudio'): 20,

    ('SFleeceTopStudio', 'FleeceStudio' ):		18    ,
    ('SFleeceTopStudio', 'CasingStudio' ):		84    ,
    ('SFleeceTopStudio', 'LaborStudio'): 15,
    ('SFleeceTopStudio', 'FleeceScrapStudio'): - 1,


    ('PillowStudio', 'FleeceScrapStudio'): 1,
    ('PillowStudio', 'LaborStudio'): 3,

    ('BagStudio', 'MeshScrapStudio'): 1,
    ('BagStudio', 'LoopsStudio'): 1,
    ('BagStudio', 'LaborStudio'): 3
}

ord_offset = {
    'LQuiltTop':2,
    'MQuiltTop':2,
    'SQuiltTop':2,

}

ord_cost = {
    ('SBox'): 50,
    ('LBox'): 75,
('Fleece' ):  		640 ,
('Mesh'   ):  		200,
('Casing' ):		100 ,
('MLegs' )	:		40  ,
('PLegs'  ):   		100 ,
('18PRods'): 		30  ,
('24PRods'): 		36  ,
('30PRods'): 		42  ,
('36PRods'):		48  ,
('30MRods'): 		40 ,
('36MRods'): 		50,
('LaborStudio'): 		20,
('Labor'): 		5,
    ('SQuiltTop'): 15,
    ('MQuiltTop'): 25,
    ('LQuiltTop'): 35,
    ('JaneyToDoug'): 50,
    ('DougToJaney'): 30
 }

ord_qty = {
    ("SBox"): 20,
    ('LBox'): 120,
('Fleece' ):  	1440,
('Mesh'   ):  	3600,
('Casing' ):	1800,
('MLegs' )	:	40 	,
('PLegs'  ):   	100 ,
('18PRods'): 	25 	,
('24PRods'): 	25 	,
('30PRods'): 	25 	,
('36PRods'):	25 	,
('36MRods'): 	5	,
('30MRods'): 	5 ,
('LaborStudio'): 60 ,
('Labor'): 60,
    ('SQuiltTop'): 1,
    ('MQuiltTop'): 1,
    ('LQuiltTop'): 1,
('JaneyToDoug'): 1,
    ('DougToJaney'): 1
}

min_buy = {
'30MRods': 2,
'36MRods': 2,
'LaborStudio': 4,
    ('SQuiltTop'): 3,
    ('MQuiltTop'): 3,
    ('LQuiltTop'): 3,
}

max_buy = {     #3-Dec	18-Oct	19-Oct	20-Oct	21-Oct	15-Oct
'LaborStudio' : 	[8,  8,  4,  8,  8, 8],
'Labor' : 	[10,  10,  10,  10,  10, 10],
'SendsToGarage': [1, 1, 1, 1, 1, 1],
'SendsToStudio': [1, 1, 1, 1, 1, 1]
}

baseprice = {  # product price, defaulted to 0 if not specified
    ('LargeMFleeceBed', 'Store'): 100,
('LargeMFleeceBed', 'Online'): 0,
('LargeMFleeceBed', 'DogShow'): 0,

('LargePFleeceBed', 'Store'):		60,
('LargePFleeceBed', 'Online'):		90,

('LargePMeshBed', 'Store'):		50,
('LargePMeshBed', 'Online'):	75,

('LargeMMeshBed', 'Store'):		80,

('MediumPFleeceBed', 'Store'):	50,
('MediumPFleeceBed', 'Online'):	65,

('MediumPMeshBed', 'Store'):	30,
('MediumPMeshBed', 'Online'):	45,

('SmallPFleeceBed', 'Store'):	30,
('SmallPFleeceBed', 'Online'):	40,
('SmallPFleeceBed', 'DogShow'):	65,

('SmallPMeshBed', 'Store'):		20,
('SmallPMeshBed', 'Online'):	30,
('SmallPMeshBed', 'DogShow'):	45,

('LFleeceTop', 'Store'):		30,
('LFleeceTop', 'Online'):		40,

('MFleeceTop', 'Store'):	25,
('MFleeceTop', 'Online'):	35,

('SFleeceTop', 'Store'):	15,
('SFleeceTop', 'Online'):	25,
('SFleeceTop', 'DogShow'):	40,

('18PRods', 'Store'):		3,

('24PRods', 'Store'):  4,

('30PRods', 'Store'):	5,

('30MRods', 'Store'):	8,

('36PRods', 'Store'):	6,

('36MRods', 'Store'):	12,

('PLegs', 'Store'):		3,

('MLegs', 'Store'):		5,

('Pillow', 'Store'):	10,
('Pillow', 'Online'):	12,
('Pillow', 'DogShow'):	15,

('Bag', 'Store'):	8,
('Bag', 'Online'):	10,
('Bag', 'DogShow'):	10,
}


p_disc = .02

#product demand defaulted to 0 if not given here
demand =  {       		      #3-Dec	18-Oct	19-Oct	20-Oct	21-Oct	15-Oct
    ('LargeMFleeceBed', 'Store')  : 	[4,  4,  4,  4,  4, 2],
    ('LargePFleeceBed', 'Store')  : 	[5,  5,  5,  5,  5, 2],
    ('LargePMeshBed', 'Store') 	  : 	[6,  6,  6,  6,  6, 2],
    ('LargeMMeshBed', 'Store') 	  : 	[1,  2,  3,  4,  5, 2],
    ('MediumPFleeceBed', 'Store') : 	[6,  7,  8,  9,  10, 2],
    ('MediumPMeshBed', 'Store')   : 	[6,  7,  8,  9,  10, 2],
    ('SmallPFleeceBed', 'Store')  : 	[6,  7,  8,  9,  10, 2],
    ('SmallPMeshBed', 'Store') 	  : 	[5,  6,  7,  8,  9, 2],
    ('LFleeceTop', 'Store') 	  : 	[10,  0,  0, 0,  10, 2],
    ('MFleeceTop', 'Store') 	  : 	[5,  0,  0, 0,  5, 2],
    ('SFleeceTop', 'Store') 	  : 	[8,  0,  0, 0,  8, 2],
    ('18PRods', 'Store') 	      : 	[2,  0,  0, 0,  0, 0],
    ('24PRods', 'Store') 	      : 	[4,  0,  0, 0,  0, 0],
    ('30PRods', 'Store') 	      : 	[6,  0,  0, 0,  0, 0],
    ('30MRods', 'Store') 	      : 	[8,  0,  0, 0,  0, 0],
    ('36PRods', 'Store') 	      : 	[10,  0,  0, 0,  0, 0],
    ('36MRods', 'Store') 	      : 	[5,  0,  0, 0,  0, 0],
    ('PLegs', 'Store') 	          : 	[5,  0,  0, 0,  0, 0],
    ('MLegs', 'Store') 	          : 	[10,  0,  0, 0,  0, 0],
    ('Pillow', 'Store') 	      : 	[12,  14,  15,  15,  15,5],


    ('SmallPFleeceBed', 'DogShow'):     [0, 0, 0, 0, 10, 0],
    ('SmallPMeshBed', 'DogShow') : 	    [0, 0, 0, 0, 15, 0],
    ('SFleeceTop', 'DogShow') 	  : 	[0, 0, 0, 0, 5, 0],
    ('Pillow', 'DogShow') 	      : 	[0, 0, 0, 0, 20, 0],
    ('Bag', 'DogShow') 	          : 	[0, 0, 0, 0, 30, 0],


        ("LargePFleeceBed",'Online'): [1,	2,	3,	1,	1, 1],
("LargePMeshBed",'Online'): [2,	2,	2,	2,	3, 3],
("MediumPFleeceBed",'Online'): [3,	2,	3,	1,	2, 2],
("MediumPMeshBed",'Online'): [1,	2,	4,	1,	3, 3],
("SmallPFleeceBed",'Online'): [2,	2,	3,	2,	2, 2],
("SmallPMeshBed",'Online'): [3,	2,	2,	3,	3, 3],
("LFleeceTop",'Online'): [1,	2,	3,	4,	5, 5],
("MFleeceTop",'Online'): [2,	3,	5,	6,	6, 6],
('SFleeceTop','Online'): [3,	2,	4,	7,	7, 7],
('Pillow','Online'): [1,	3,	2,	2,	3, 3],

}
#scrap_pen = {  # resource scrap penalty default 0
    #'Fleece': - .13888888}

supply = {  # resource availability default 0
('Mesh', '3-Dec'): 1440,
('Fleece', '3-Dec'): 2880,
('Casing', '3-Dec'): 7200,

('PLegs', '3-Dec'): 60,
('MLegs', '3-Dec'): 32,

('36PRods', '3-Dec'): 8,
('36MRods', '3-Dec'): 12,
('30PRods', '3-Dec'): 7,
('30MRods', '3-Dec'): 6,
('24PRods', '3-Dec'): 12,
('18PRods', '3-Dec'): 10,


}

sub_usage = {  # Define the set SUB_TRIPLES as the list is processed
    ('LMeshTop', 'Casing', 'Loops'): 26,
    ('MMeshTop', 'Casing', 'Loops'): 22,
    ('SMeshTop', 'Casing', 'Loops'): 18,
}


init_stoc = {}
scrap_pen = {}
make_pen = {}
sub_pen = {}
stoc_pen = {}


data_dict = {
    "MATERIAL": MATERIAL,
    "CAPACITY": CAPACITY,
    "CUSTOMER": CUSTOMER,
    "NO_LATE": NO_LATE,
    "LOCATION": LOCATION,
    "LOW_PRIORITY": LOW_PRIORITY,
    "IS_SHIPPED": IS_SHIPPED,
    "BUYSandSHIPS": BUYSandSHIPS,
    "TIME": TIME,
    "NEEDS_LARGE_BOX": NEEDS_LARGE_BOX,
    "HAS_OFFSET": HAS_OFFSET,
    "usage": usage,
    "ord_offset": ord_offset,
    "sub_usage": sub_usage,
    "baseprice": baseprice,
    "p_disc": p_disc,
    "demand": demand,
    "supply": supply,
    "ord_qty": ord_qty,
    "ord_cost": ord_cost,
    "init_funds": init_funds,
    "min_buy": min_buy,
    "max_buy": max_buy,
    "init_stoc": init_stoc,
    "scrap_pen": scrap_pen,
    "make_pen": make_pen,
    "stoc_pen": stoc_pen,
    "sub_pen" : sub_pen,
}




