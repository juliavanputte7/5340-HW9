
# Data
MATERIAL = {'LargeMMeshBed', 'LargePMeshBed', 'MediumPMeshBed', 'SmallPMeshBed',
            'LargeMFleeceBed', 'LargePFleeceBed', 'MediumPFleeceBed', 'SmallPFleeceBed',
            'LMFrame', 'LPFrame', 'MPFrame', 'SPFrame',
            'LFleeceTop', 'MFleeceTop', 'SFleeceTop', 'LMeshTop', 'MMeshTop', 'SMeshTop',  # set of products
            'Mesh', 'Fleece', 'PLegs', 'Casing', '36PRods', '30PRods', '24PRods', '18PRods', 'cash'
            'Loops', 'MLegs', '36MRods', '30MRods', 'FleeceScrap', 'Pillow', 'MeshScrap', 'Bag'}

CUSTOMER = {'Store', 'Online', 'DogShow'}
LOW_PRIORITY = {'DogShow'}     # subset oc customers, low priority
NO_LATE = {'DogShow'}          #subset of customers, can't ship late
IS_SHIPPED = {'Store'}
BUYSandSHIPS =  {'DougTime'}

CAPACITY = {'DougTime', 'JaneyTime'}
TIME = ['17-Oct', '18-Oct', '19-Oct', '20-Oct', '21-Oct']

init_funds = 2000

usage = {  # list for BOM  USUAL INPUT FORMAT FROM MRP SYSTEM
    ('LargeMMeshBed', 'LMeshTop'): 1,
    ('LargeMMeshBed', 'LMFrame'): 1,
    ('LargeMMeshBed', 'DougTime'): 15,

    ('LargePMeshBed', 'LMeshTop' ):  1	,
    ('LargePMeshBed', 'LPFrame' ):	1,
    ('LargePMeshBed', 'DougTime' ):	12,

    ('LargeMFleeceBed', 'LFleeceTop' ):	 1	,
    ('LargeMFleeceBed', 'LMFrame' ):	1	,
    ('LargeMFleeceBed', 'DougTime' ):	15	,

    ('LargePFleeceBed'   , 'LFleeceTop' ):	1	,
    ('LargePFleeceBed'   , 'LPFrame' 	):	1	,
    ('LargePFleeceBed', 'DougTime' ):	12	,

    ('MediumPFleeceBed'   , 'MFleeceTop'): 	1	,
    ('MediumPFleeceBed'   , 'MPFrame' 	):	1	,
    ('MediumPFleeceBed'   , 'DougTime' ):	8	,

    ('MediumPMeshBed'     , 'MMeshTop' 	) :1,
    ('MediumPMeshBed', 'MPFrame' ) :1,
    ('MediumPMeshBed'   , 'DougTime' ):	8	,

    ('SmallPMeshBed', 'SMeshTop' ) :1,
    ('SmallPMeshBed', 'SPFrame' ):	1	,
    ('SmallPMeshBed', 'DougTime' ):	5	,

    ('SmallPFleeceBed'    , 'SFleeceTop'): 	1	,
    ('SmallPFleeceBed'    , 'SPFrame' 	):	1	,
    ('SmallPFleeceBed', 'DougTime'): 5,

    ('LMeshTop', 'Mesh'	):	 36	  ,
    ('LMeshTop', 'Casing' ):	132   ,
    ('LMeshTop', 'DougTime'): 	12 ,

    ('MMeshTop', 'Mesh' 	):		24 ,
    ('MMeshTop', 'Casing' 	):	108    ,
    ('MMeshTop', 'DougTime'): 8,

    ('SMeshTop', 'Mesh '	):		18 ,
    ('SMeshTop', 'Casing' 	):	84     ,
    ('SMeshTop', 'DougTime' ):		4,
    ('SMeshTop', 'MeshScrap'): 		-1,

    ('LFleeceTop', 'Fleece'): 36,
    ('LFleeceTop', 'Casing'): 132,
    ('LFleeceTop', 'DougTime'):	25,

    ('MFleeceTop', 'Fleece'): 24,
    ('MFleeceTop', 'Casing'): 108,
    ('MFleeceTop', 'DougTime'): 20,

    ('SFleeceTop', 'Fleece' ):		18    ,
    ('SFleeceTop', 'Casing' ):		84    ,
    ('SFleeceTop', 'DougTime'): 15,
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
    ('Pillow', 'DougTime'): 3,

    ('Bag', 'MeshScrap'): 1,
    ('Bag', 'Loops'): 1,
    ('Bag', 'DougTime'): 3
}

ord_cost = {
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
('JaneyTime'): 		20,
('DougTime'): 		5
 }

ord_qty = {
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
('JaneyTime'): 60 ,
('DougTime'): 60
}

min_buy = {
'30MRods': 2,
'36MRods': 2,
'JaneyTime': 4
}

max_buy = {     #17-Oct	18-Oct	19-Oct	20-Oct	21-Oct	15-Oct
'JaneyTime' : 	[8,  8,  0,  8,  8],
'DougTime' : 	[10,  10,  10,  10,  10],
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
demand =  {       		      #17-Oct	18-Oct	19-Oct	20-Oct	21-Oct	15-Oct
    ('LargeMFleeceBed', 'Store')  : 	[4,  4,  4,  4,  4],
    ('LargePFleeceBed', 'Store')  : 	[5,  5,  5,  5,  5],
    ('LargePMeshBed', 'Store') 	  : 	[6,  6,  6,  6,  6],
    ('LargeMMeshBed', 'Store') 	  : 	[1,  2,  3,  4,  5],
    ('MediumPFleeceBed', 'Store') : 	[6,  7,  8,  9,  10],
    ('MediumPMeshBed', 'Store')   : 	[6,  7,  8,  9,  10],
    ('SmallPFleeceBed', 'Store')  : 	[6,  7,  8,  9,  10],
    ('SmallPMeshBed', 'Store') 	  : 	[5,  6,  7,  8,  9],
    ('LFleeceTop', 'Store') 	  : 	[10,  0,  0, 0,  10],
    ('MFleeceTop', 'Store') 	  : 	[5,  0,  0, 0,  5],
    ('SFleeceTop', 'Store') 	  : 	[8,  0,  0, 0,  8],
    ('18PRods', 'Store') 	      : 	[2,  0,  0, 0,  0],
    ('24PRods', 'Store') 	      : 	[4,  0,  0, 0,  0],
    ('30PRods', 'Store') 	      : 	[6,  0,  0, 0,  0],
    ('30MRods', 'Store') 	      : 	[8,  0,  0, 0,  0],
    ('36PRods', 'Store') 	      : 	[10,  0,  0, 0,  0],
    ('36MRods', 'Store') 	      : 	[5,  0,  0, 0,  0],
    ('PLegs', 'Store') 	          : 	[5,  0,  0, 0,  0],
    ('MLegs', 'Store') 	          : 	[10,  0,  0, 0,  0],
    ('Pillow', 'Store') 	      : 	[12,  14,  15,  15,  15],


    ('SmallPFleeceBed', 'DogShow'):     [0, 0, 0, 0, 10],
    ('SmallPMeshBed', 'DogShow') : 	    [0, 0, 0, 0, 15],
    ('SFleeceTop', 'DogShow') 	  : 	[0, 0, 0, 0, 5],
    ('Pillow', 'DogShow') 	      : 	[0, 0, 0, 0, 20],
    ('Bag', 'DogShow') 	          : 	[0, 0, 0, 0, 30],

}
#scrap_pen = {  # resource scrap penalty default 0
    #'Fleece': - .13888888}

supply = {  # resource availability default 0
('Mesh', '17-Oct'): 1440,
('Fleece', '17-Oct'): 2880,
('Casing', '17-Oct'): 7200,

('PLegs', '17-Oct'): 60,
('MLegs', '17-Oct'): 32,

('36PRods', '17-Oct'): 8,
('36MRods', '17-Oct'): 12,
('30PRods', '17-Oct'): 7,
('30MRods', '17-Oct'): 6,
('24PRods', '17-Oct'): 12,
('18PRods', '17-Oct'): 10,


}

sub_usage = {  # Define the set SUB_TRIPLES as the list is processed
    ('LMeshTop', 'Casing', 'Loops'): 26,
    ('MMeshTop', 'Casing', 'Loops'): 22,
    ('SMeshTop', 'Casing', 'Loops'): 18,
    ('LFleeceTop', 'DougTime', 'JaneyTime'): 20,
    ('MFleeceTop', 'DougTime', 'JaneyTime'): 15,
    ('SFleeceTop', 'DougTime', 'JaneyTime'):  10,
    ('LMeshTop', 'DougTime', 'JaneyTime'): 15,
    ('MMeshTop', 'DougTime', 'JaneyTime'): 10,
    ('SMeshTop', 'DougTime', 'JaneyTime'):  5,
    ('Pillow', 'DougTime', 'JaneyTime'):  3,
    ('Bag', 'DougTime', 'JaneyTime'):  3,
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
    "LOCATION": {},
    "LOW_PRIORITY": LOW_PRIORITY,
    "IS_SHIPPED": IS_SHIPPED,
    "BUYSandSHIPS": BUYSandSHIPS,
    "TIME": TIME,
    "NEEDS_LARGE_BOX": {},
    "HAS_OFFSET": {},
    "usage": usage,
    "ord_offset": {},
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




