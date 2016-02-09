# land-demo


Quickstart
----------

Then run the following commands to bootstrap your environment.

```
mkvirtualenv --python=/path/to/required/python/version [appname]
```

Install python requirements.
```
pip install -r requirements/dev.txt
```

To run locally you will need a local mongodb to hold premises data. This can be loaded using a management command. Before you can run the command (or the application) set some environment variables.

The keen eyed will notice that this application does not directly access register data at runtime. Instead the management command fetches data from registers and stashes it away locally. Want fresh data? Drop and reload.

The following environment variables are all required:

```
export SETTINGS='config.DevelopmentConfig'
export PREMISES_REGISTER='http://premises.preview.openregister.org'
export MONGO_URI='mongodb://localhost:27017'
export PRODUCTS_OF_ANIMAL_ORIGIN_PREMISES='http://products-of-animal-origin-premises.openregister.org'
export PRODUCTS_OF_ANIMAL_ORIGIN_SECTION='http://products-of-animal-origin-section.openregister.org'
export PRODUCTS_OF_ANIMAL_ORIGIN_ACTIVITY='http://products-of-animal-origin-activity.openregister.org'
export COMPANIES_HOUSE_API_KEY='[get yourself an api key - see below - and probably not check it into version control]'
```

For a Companies House api key go to [https://developer.companieshouse.gov.uk/](https://developer.companieshouse.gov.uk/) and register.

Once that this all done you can load data:

```
source environment.sh
python manage.py load_local_data
```

That will run for a bit and load some 550 odd records. Once doe you can run the app.

```
./run.sh
```


Deployment
----------

In your production environment, make sure the ``SETTINGS`` environment variable is set to ``config.Config``.

