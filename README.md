# Star Wars Api Data Scraper

### Initial setup on Windows
First create new virtual environment in root directory, and install all required packages from `requirements.txt` file

- Create env named env: `python -m venv venv `
- Activate environment: `venv\Scripts\activate`
- Install all packages: `pip install -r requirements.txt`

You could also simply use `docker-compose.yaml` file.

### Config values:

- **output_path** - This is absolute path value, where output should be saved. If script can't find that path, then it is producing data.yaml file in root directory. Example: `"output_path": "/app"`
- **max_person**: (**MIN 1** - **MAX 82**) This is range of characters pool (and their numbers) from which script will randomize and add to data.yaml output file. Example: `"max_person": 82`
- **max_planets**: (**MIN 1** - **MAX 60**) This is range of planets pool (and their numbers) from which script will randomize and add to data.yaml output file. Example: `"max_planets": 60`
- **count_of_people_and_planet**: (**MIN 1** - **MAX 60***) This is exact number of peoples, and planets that script will save to data.yaml file before finishing its job. ***This number can't be higher than lower value of max_planets or max_person. Example: "max_person": 82, "max_planets": 32, "count_of_people_and_planet": 32** 

### `config.json` should not be moved from root directory.<br/><br/> It must be placed next to `config.py` file

### Running script:

#### You can simply run this script in two ways:

- Running `python -m main.py ` from **root directory**
- Running `docker compose up ` also from **root directory**

#### Script does have command line argument `--interval` which is set to 5 by default and it set number of seconds between each script iteration
Example:
`python -m main.py --interval 1` It will set interval time sleep to 1 second.

You can run tests simply by running `pytest` in root directory
 