from app4 import app, db, Product

with app.app_context():
    db.drop_all()
    db.create_all()

    items = [
        Product(
            name="Wallnuts",
            brand="DMM",
            price=76.50,
            description="A versatile tapered nut featuring grooved faces and a curved profile for stable placements in irregular rock.",
            image="DMM_Wallnut_1.png",
            eco_impact=1.2
        ),
        Product(
            name="Torque Nuts",
            brand="DMM",
            price=94.50,
            description="A versatile hex for cracks of several sizes and shapes, featuring an integrated extendable sling and lightweight construction.",
            image="a1741-44-torque-nut-set-1-4_2048x.png",
            eco_impact=1.8
        ),
        Product(
            name="Alloy Offsets",
            brand="DMM",
            price=71.00,
            description="A specialised nut with an asymmetrical taper for flared cracks and pin scars, featuring grooved faces and dual-orientation design.",
            image="A1817-21AA-HB-Alloy-Offsets-Set-7.png",
            eco_impact=1.5
        ),
        Product(
            name="Carabiner Set",
            brand="Black Diamond",
            price=45.00,
            description="A set of lightweight oval carabiners ideal for racking gear, pulleys, and aid climbing setups.",
            image="black-diamond-litewire-rackpack-snapgate-carabiner.jpg",
            eco_impact=0.9
        ),
    ]

    db.session.add_all(items)
    db.session.commit()
    print("Database seeded successfully!")