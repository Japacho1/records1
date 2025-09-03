from django.db import migrations

def add_initial_tenants(apps, schema_editor):
    Tenant = apps.get_model('files', 'Tenant')
    tenants = [
        "AGHAKHAN", "AIRTEL", "ALLADIN", "ANIQ FASHION", "ANMOL", "AQUA PET", "ARTCAFFE RESTAURANT", "ASHLEYS FURNITURE",
        "ASHLEYS SALON", "AUTO ELEKTRA", "AVNI", "BAGGI MEN", "BASIC INTIMATES", "BIG SQUARE", "BIKES AND SPORTS", 
        "BURGER KING", "CAMBRIDGE OPTICANS", "CAPITAL FM", "CARREFOUR", "CEITEI", "CENTURION PHARMACY", "CHICKEN INN", 
        "CHINA SQUARE", "CINAMON CAFFE", "COFFEE HOUSE", "COOPERATIVE BANK", "DECATHLON", "DELI MAHAL", "EUGEN KLEIN", 
        "FEEL NZURI", "FLO", "FRAGRANCE LOUNGE", "FUNSCAPES", "GALITOS", "GAMETRONICS", "GOING OUTDOOR", "GYM", 
        "HEALTHY U", "HLA", "HORTON DENTAL", "HOT YOGA STUDIO", "HOUSE WIVES PARADISE", "INFINI", "INKLESS IS MORE", 
        "IPLACE", "ISTANBUL PALACE", "ITALIAN DESIGNER", "JAFFS OPTICA", "JAMBO WRAP", "JAVA EXPRESS", 
        "JOY CRUSH /TA CRISPY CHICKEN", "JTC", "JUMBO FOAM", "JUNCTION FOREX", "KCB", "KIPUSA", "LC DREAM", 
        "LC WAIKIKI", "LEO HAIR SALON", "LEVIS", "LINTONS", "LOCKWOOD FURNITURE", "LOTTO SPORTS", "LOUIS FERALD", 
        "MAIYAN", "MANIX", "MICKEYS", "MINISO", "MORE N MORE", "MOSQUE", "MR. WOK", "NCBA", "NRG RESTAURANT", 
        "OPPO", "ORCA DECO", "PANDA TEA", "PARISLAND", "PIERRE CARDIN", "PLATFORM", "PORTAL PHARMACY", 
        "RADIANCE LIGHTS SHOP", "REVIVE FASHION", "RIVERBANK", "ROUND LIQUORS", "SAFARICOM", "SANAA AFRICA", 
        "SIDIAN BANK", "SMART BABY", "SPUR RESTAURANT", "STANBIC BANK", "SUPAW PETS", "SWAROVSKI", "TAJ GEMS", 
        "TBC", "TECHNO", "TOMOCCA RESTAURANT", "TOYZOONA", "ULTRACLEAN LAUNDROMART", "UMOJA SHOE", "VICTORIA CARPETS", 
        "VIVO", "XIMI VOGUE", "YOKORA SPORTS", "ZOPO MAN"
    ]

    for name in tenants:
        Tenant.objects.create(name=name, tenant_type='tenant')

class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),  # Replace with your actual previous migration
    ]

    operations = [
        migrations.RunPython(add_initial_tenants),
    ]
