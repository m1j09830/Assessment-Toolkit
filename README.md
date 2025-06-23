# Assessment-Toolkit

## Python Compatibility

✅ **Python 3.13 Compatible!** This project supports Python 3.9 through 3.13.

See [PYTHON_313_COMPATIBILITY.md](./PYTHON_313_COMPATIBILITY.md) for details on recent updates.

## Dependencies

The following tools must be installed on the system:
* Aquatone (https://github.com/michenriksen/aquatone)
* Mikto (https://github.com/ChrisTruncer/mikto.git)
* Nmap
* Nuclei (https://github.com/projectdiscovery/nuclei.git)
* Shodan CLI (https://cli.shodan.io/) - The tool will install this for you; however, you will need a valid Shodan API key prior to using the shodan_scans function. 

## Install
Assessment-Toolkit can be installed by cloning this repository and running `pip3 install .` and subsequently executed from PATH with Assessment-Toolkit

## Usage

`scoper` - Create an Inscope file which will account for any excluded targets if applicable.  It is highly advised to run scoper first before running any of the subsequent functions.

`Assessment-Toolkit -o scoper -i <Target_File> -e <Exclude_File> -p <Project_Name>`

`discovery` - Run nmap discovery scans against provided target list.

`Assessment-Toolkit -o discovery -i <Target_File> -p <Project_Name>`

`full` - Run nmap full port scans against provided target list.

`Assessment-Toolkit -o full -i <Target_File> -p <Project_Name>`

`aquatone` - Run aquatone scans against provided web application list.

`Assessment-Toolkit -o aquatone -i <Target_File> -p <Project_Name>`

`nikto` - Run nikto scans against provided web application list.

`Assessment-Toolkit -o nikto -i <Target_File> -p <Project_Name>`

`shodan_scans` - Use Shodan API to check for open ports within provided target list. 

`Assessment-Toolkit -o shodan_scans -i <Target_File> -p <Project_Name>`

`nuclei_scans` - Run Nuclei vulnerability scanner against provided target list. Can be used with or without `uncover engine`. Shodan API key required for `uncover engine` option.

`Assessment-Toolkit -o nuclei_scans -i <Target_File> -p <Project_Name>`

`external_scans` - Will run nmap discovery, aquatone discovery, nmap full port, aquatone full port, and nikto scans on provided target list.

`Assessment-Toolkit -o external_scans -i <Target_File> -p <Project_Name>`

`internal_scans` - Will run nmap discovery, aquatone discovery, nmap full port and aquatone full port on provided target list.

`Assessment-Toolkit -o internal_scans -i <Target_File> -p <Project_Name>`

## Development
Assessment-Toolkit uses Poetry to manage dependencies. Install from source and setup for development with:
```
git clone https://github.com/m1j09830/Assessment-Toolkit
cd Assessment-Toolkit
poetry install
poetry run Assessment-Toolkit --help
```

## Credits
https://github.com/coffeegist/cookiecutter-app