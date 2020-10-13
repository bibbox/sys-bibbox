
#!/bin/bash

function bibbox-installApp() 
{
        var1="'$1'"
        var1ch=$1
        var2="'$2'"
        var2ch=$2
        var3="'$3'"


        #while [ "$var1ch" != "" ]; do
        case $var1ch in
                -h | --help )           installusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift
        #done
        declare name
        name=$(sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.getAppName('"$var2"')' 2>&1)
        declare keylist
	declare paramlist
        params=$(curl https://raw.githubusercontent.com/bibbox/"${name}"/master/.env)
        #echo $appname
	sed -n s/' '/'='/g <<< $params
        #echo https://raw.githubusercontent.com/bibbox/${name}/master/.env
        echo Please enter user specifications!
        echo This user specifications are used for the login later.
	#ext = begin
	keylist="'"
        paramlist="'"
#	echo $params params
#	IFS=' '
#        read -a line <<< $params
#	echo ${line} line
	for item in $params
        do
#	  echo $params
          IFS='='
          read -a strarr <<< $item
#	  echo ch1
#	  echo $item
#	  echo ch2
#	  echo $strarr
#	  echo ch3
#	  echo ${strarr[0]}
	  IFS=$'\n'
          read -a out <<< $item
#	  echo ${out[0]} out
          if [ ${strarr[0]} != 'PORT' ] && [ ${strarr[0]} != 'INSTANCE' ] 
          then
#	    echo check
#	    echo $params
#	    echo check1
 #           echo ${item[0]}
#	    echo check2
	    echo ${strarr[0]}:
            read param
	    v2=$param
	    v1=${strarr[0]}
	    keylist="$keylist;$v1"
	    paramlist="$paramlist;$v2"
	    fi
	done
        keylist="$keylist'"
        paramlist="$paramlist'"

        

#	echo $keylist
#	echo $paramlist


        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.installApp('"$paramlist"','"$keylist"','"$var1"','"$var2"','"$var3"',CLI=True)'



}

function bibbox-startApp() 
{
	var="'$1'"
        var1ch=$1

        case $var1ch in
                -h | --help )           startusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

	sudo python3 -c 'import sys; sys.path.insert(1, "//opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.startApp('"$var"')'
}

function bibbox-stopApp() 
{
        var="'$1'"
        var1ch=$1

        case $var1ch in
                -h | --help )           stopusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.stopApp('"$var"')'
}

function bibbox-removeApp() 
{
        var="'$1'"
        var1ch=$1

        case $var1ch in
                -h | --help )           removeusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.removeApp('"$var"')'
}

function bibbox-getStatus() 
{
        var="'$1'"
        var1ch=$1

        case $var1ch in
                -h | --help )           statususage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.getStatus('"$var"')'
}

function bibbox-copyApp() 
{
        var1="'$1'"
	var2="'$2'"
        var1ch=$1

        case $var1ch in
                -h | --help )           copyusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.copyApp('"$var1"','"$var2"')'
}

function bibbox-listApps() 
{
        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.listApps()'

        while [ "$1" != "" ]; do
        case $1 in
                -h | --help )           listusage
                                        ;;
                -v | --version | version )  version
                                        ;;
                * )                     usage
                                        error_exit "Parameters not matching"
        esac
        shift
        done

}

function bibbox-listInstalledApps() 
{

        case $1 in
                -h | --help )           installusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.listInstalledApps()'
}

function bibbox-startBibbox() 
{

        case $1 in
                -h | --help )           startbibboxusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.startBibbox()'
}

function bibbox-stopBibbox() 
{

        case $1 in
                -h | --help )           stopbibboxusage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift

        sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import bibboxbackend; x=bibboxbackend.MainFunctions(); x.stopBibbox()'
}

function bibbox() 
{       
        var1=$1

        case $var1 in
                -h | --help )           usage
                                        return
                                        ;;
                -v | --version | version )  version
                                        return
                                        
        esac
        shift
}

function clean_up() {

	# Perform program exit housekeeping
	# Optionally accepts an exit status
	
	exit $1
}

function error_exit()
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	clean_up 1
}

function installusage()
{

    echo "DESCRIPTION"
    echo "Installs a new bibbox app with a specific unique name"
    echo ""
    echo "SYNTAX"
    echo "bibbox-installApp <instancename> <appname> <version>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-installApp  SeedDMS master"
    echo ""
    echo "PARAMETERS    
----------

paramList: array
        list of environment variables that are defined in the .env file in the repository of the application

instanceName : str
        The instance name of the application that is used 

appName : str
        The (github) name of the application that is used 

version : str
        The wanted version of the application that is used 
        The version name is considered optional. If no version name is given,
        the latest version of the application is installed.
"

}

function startusage()
{

    echo "DESCRIPTION"
    echo "Starts the wanted BiBBox app container"
    echo ""
    echo "SYNTAX"
    echo "bibbox-startApp <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-startApp seeddmstest"
    echo ""
    echo "PARAMETERS
----------

instanceName : str
        The instance name of the application that is used 

Raises:
-------

Returns:
-------"
}

function stopusage()
{

    echo "DESCRIPTION"
    echo "Stops the wanted BiBBox app container"
    echo ""
    echo "SYNTAX"
    echo "bibbox-startApp <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-stopApp seeddmstest"
    echo ""
    echo "PARAMETERS
----------

instanceName : str
        The instance name of the application that is used 

Raises:
-------

Returns:
-------"
}

function removeusage()
{

    echo "DESCRIPTION"
    echo "Removes the wanted BiBBox app container"
    echo ""
    echo "SYNTAX"
    echo "bibbox-removeApp <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-removeApp seeddmstest"
    echo ""
    echo "PARAMETERS
----------

instanceName : str
        The instance name of the application that is used 

Raises:
-------

Returns:
-------"
}

function statususage()
{

    echo "DESCRIPTION"
    echo "Returns the current status of the wanted application"
    echo ""
    echo "SYNTAX"
    echo "bibbox-getStatus <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-getStatus seeddmstest"
    echo ""
    echo "PARAMETERS
----------

instanceName : str
        The instance name of the application that is used 

Raises:
-------

Returns:
-------

status : str
        The current status of the application that is used "
}

function copyusage()
{

    echo "DESCRIPTION"
    echo "Copies the wanted application"
    echo ""
    echo "SYNTAX"
    echo "bibbox-copyApp <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-copyApp oldappname newappname"
    echo ""
    echo "PARAMETERS
----------

instanceName : str
        The instance name of the application that is used 

newName : str
        The new name of the application that is used 

Raises:
-------

Returns:
------- "
}

function listusage()
{

    echo "DESCRIPTION"
    echo "Lisis all available applications"
    echo ""
    echo "SYNTAX"
    echo "bibbox-listApps"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-listApps"
    echo ""
    echo "PARAMETERS
----------

Raises:
-------

Returns:
-------
appslist: json object
        The list of all available apps as json string"
}

function listinstalledusage()
{

    echo "DESCRIPTION"
    echo "Lisis all installed applications"
    echo ""
    echo "SYNTAX"
    echo "bibbox-listInstalledApps"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-listInstalledApps"
    echo ""
    echo "PARAMETERS
----------

Raises:
-------

Returns:
-------
appslist: json object
        The list of all installed apps with the corresponding instance name as json string"
}

function startbibboxusage()
{

    echo "DESCRIPTION"
    echo "Starts the main bibbox system"
    echo ""
    echo "SYNTAX"
    echo "bibbox-startBibbox"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-startBibbox"
    
}

function stopbibboxusage()
{

    echo "DESCRIPTION"
    echo "Stops the main bibbox system"
    echo ""
    echo "SYNTAX"
    echo "bibbox-stopBibbox"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-stopBibbox"
    
    
}


function usage()
{

    echo "DESCRIPTION"
    echo "This module is made to controll the BiBBoX software through a CLI."
    echo "The following functiuons are available:"
    echo "bibbox-installApp"
    echo "bibbox-startApp"
    echo "bibbox-stopApp"
    echo "bibbox-copyApp"
    echo "bibbox-listApps"
    echo "bibbox-listInstalledApps"
    echo "bibbox-removeApp"
    echo "bibbox-getStatus"
    echo "bibbox-startBibbox"
    echo "bibbox-stopBibbox"
    echo ""
    echo "For a detailed function documentation please enter:"
    echo "<functionname> -h or <functionname> --help"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox -h "
    echo ""
    echo "IMPLEMENTATION"
    echo "version                       version 1.0"
 #   echo "author                        Stefan Herdy"
    echo "copyright                     Copyright  Medical University of Graz"
    echo "license                       GNU General Public License"
}

function version()
{
  echo "Version: 1.0"
  echo "BIBBOX Version: 1.0"
}






#installApp seeddms22 app-seeddmsTNG master
#stopApp seeddms10
#startApp seeddms10
#getStatus seeddms10
#copyApp seeddms10 seeddms11
#removeApp seeddms10
#listApps
#listInstalledApps
