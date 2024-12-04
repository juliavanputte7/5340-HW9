doug_names = {'LargeFleeceTop',
             'MediumFleecTop',
             'SmallFleeceTop',
             'LargeMeshTop',
             'MediumMeshTop',
             'SmallMeshTop',
             'Fleece Pillow',
             '18PlasticRod',
             '24PlasticRod',
             '30PlasticRpd',
             '30MetalRod',
             '36PlasticRod',
             '36MetalRod',
             'Plastic Legs',
             'Metal Legs',
             'Fleece (yards)',
             'Mesh (yards)',
             'Fabric bundle',
             'Loops',
             'Casing (yards)',
             'Sew (hr)',
             'Serge (hr)',
             'LargeMetalFleece',
             'LargePlatic Fleece',
             'LargePlasticMesh',
             'LargeMetalMesh',
             'MediumFleece',
             'MediumMesh',
             'SmallFleece',
             'SmallMesh',
             'LargeFleeceTop',
             'MediumFleecTop',
             'SmallFleeceTop',
             '18PlasticRod',
             '24PlasticRod',
             '30PlasticRpd',
             '30MetalRod',
             '36PlasticRod',
             '36MetalRod',
             'Plastic Legs',
             'Metal Legs',
             'Small Pillow',
             'SmallFleece',
             'SmallMesh',
             'SmallFleeceTop',
             'Small Pillow',
             'Small quilt bed',
             'Spoiled dog bundle',
             'small quilt top',
             'LargePlatic Fleece',
             'LargePlasticMesh',
             'MediumFleece',
             'MediumMesh',
             'SmallFleece',
             'SmallMesh',
             'LargeFleeceTop',
             'MediumFleecTop',
             'SmallFleeceTop',
             'Small Pillow',
             'Large bundle',
             'Medium bundle',
             'small bundle'}

data_names = {'LargeMMeshBed', 'LargePMeshBed', 'MediumPMeshBed', 'SmallPMeshBed',
            'LargeMFleeceBed', 'LargePFleeceBed', 'MediumPFleeceBed', 'SmallPFleeceBed',
            'LMFrame', 'LPFrame', 'MPFrame', 'SPFrame',
            'LFleeceTop', 'MFleeceTop', 'SFleeceTop', 'LMeshTop', 'MMeshTop', 'SMeshTop',  # set of products
            'Mesh', 'Fleece', 'PLegs', 'Casing', '36PRods', '30PRods', '24PRods', '18PRods', 'cash'
            'Loops', 'MLegs', '36MRods', '30MRods', 'FleeceScrap', 'Pillow', 'MeshScrap', 'Bag'}


doug_to_data_map = {'LargeFleeceTop': 'LFleeceTop',
             'MediumFleecTop': 'MFleeceTop',
             'SmallFleeceTop': 'SFleeceTop',
             'LargeMeshTop': 'LMeshTop',
             'MediumMeshTop':'MMeshTop',
             'SmallMeshTop': 'SMeshTop',
             'Small Pillow':'Pillow',
             '18PlasticRod':'18PRods',
             '24PlasticRod':'24PRods',
             '30PlasticRpd':'30PRods',
             '30MetalRod':'30MRods',
             '36PlasticRod':'36PRods',
             '36MetalRod':'36MRods',
             'Plastic Legs':'PLegs',
             'Metal Legs':'MLegs',
             'Fleece (yards)': 'Fleece',
             'Mesh (yards)':'Mesh',
             'Fabric bundle': "TODO",
             'Loops':'Loops',
             'Casing (yards)':'Casing',
             'Sew (hr)': "TODO",
             'Serge (hr)': "TODO",
             'LargeMetalFleece':'LargeMFleeceBed',
             'LargePlatic Fleece': 'LargePFleeceBed',
             'LargePlasticMesh':'LargePMeshBed',
             'LargeMetalMesh':'LargeMMeshBed',
             'MediumFleece':'MediumPFleeceBed',
             'MediumMesh':'MediumPMeshBed',
             'SmallFleece':'SmallPFleeceBed',
             'SmallMesh':'SmallPMeshBed',}


























































stripped = [s.strip() for s in old_names]
print(stripped)