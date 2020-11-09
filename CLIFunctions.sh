
#!/bin/bash

function bibbox() 
{       
        if [[ $1 = install ]]
        then
                appname="'$2'"
                appnamech=$2
                instance="'$3'"
                instancech=$3
                version="'$4'"
                versionch=$4
                default=false
                
                for var in "$@"
                do
                        case $var in

                                -d | --default )        default=true

                        esac 
                        case $3 in
                                -h | --help )           installusage
                                                        return
                                                        ;;
                                -bv | --bibboxversion )  version
                                                        return
                                                        ;;
                                -n | --name )           instance="'$4'"
                                                        #echo step1
                                                        
                                                        ;;                      
                                -v | --version )        version="'$4'"
                                                        versionch=$4
                                                        #echo step2
                                                        
                                
                        esac
                        shift
                        

                done
                
                
                #done
                declare name
                name=$(sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.getAppName('"$appname"')' 2>&1)
                declare keylist
                declare paramlist

                params=$(curl https://raw.githubusercontent.com/bibbox/"${name}"/"$versionch"/.env)
                sed -n s/' '/'='/g <<< $params
                echo https://raw.githubusercontent.com/bibbox/${name}/$versionch/.env
                
                echo The user specifications are used for the login later.
                #ext = begin
                keylist="'"
                paramlist="'"
                if [ $default = 'false' ]
                then
                        echo Please enter user specifications!
                fi

                if [ $default = 'true' ]
                then
                        echo The selected default values are:
                fi
                
                for item in $params
                do
        
                IFS='='
                read -a strarr <<< $item
                IFS=$'\n'
                read -a out <<< $item
                if [ ${strarr[0]} != 'PORT' ] && [ ${strarr[0]} != 'INSTANCE' ] 
                then
                        if [ $default = 'false' ]
                        then
                                echo ${strarr[0]}:  '('default = ${strarr[1]}')'
                                read param
                                v2=$param
                                v1=${strarr[0]}
                                keylist="$keylist;$v1"
                                paramlist="$paramlist;$v2"
                        fi
                        

                        if [ $default = 'true' ]
                        then
                                echo ${strarr[0]}: ${strarr[1]}
                                v2=${strarr[1]}
                                v1=${strarr[0]}
                                keylist="$keylist;$v1"
                                paramlist="$paramlist;$v2"

                        fi
                fi        
                done
                keylist="$keylist'"
                paramlist="$paramlist'"

                


                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.installApp('"$paramlist"','"$keylist"','"$instance"','"$appname"','"$version"',CLI=True)'

        fi




        if [[ $1 = start ]]
                then
                var="'$2'"
                var1ch=$2

                case $var1ch in
                        -h | --help )           startusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "//opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.startApp('"$var"')'
        fi


        if [[ $1 = stop ]]
        then
                var="'$2'"
                var1ch=$2

                case $var1ch in
                        -h | --help )           stopusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.stopApp('"$var"')'
        fi

        if [[ $1 = remove ]]
        then
                var="'$2'"
                var1ch=$2

                case $var1ch in
                        -h | --help )           removeusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.removeApp('"$var"')'
        fi

        if [[ $1 = status ]]
        then
                var="'$2'"
                var1ch=$2

                case $var1ch in
                        -h | --help )           statususage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.getStatus('"$var"')'
        fi

        if [[ $1 = copy ]]
        then
                var1="'$2'"
                var2="'$3'"
                var1ch=$2

                case $var1ch in
                        -h | --help )           copyusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.copyApp('"$var1"','"$var2"')'
        fi

        if [[ $1 = listApps ]]
        then
                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.listApps()'

                while [ "$2" != "" ]; do
                case $2 in
                        -h | --help )           listusage
                                                ;;
                        -v | --version | version )  version
                                                ;;
                        * )                     usage
                                                error_exit "Parameters not matching"
                esac
                shift
                done

        fi

        if [[ $1 = listinstances ]]
        then

                case $2 in
                        -h | --help )           installusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.listInstalledApps()'
        fi

        if [[ $1 = startSystem ]]
        then

                case $2 in
                        -h | --help )           startbibboxusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.startBibbox()'
        fi

        if [[ $1 = restartSystem ]]
        then
                case $2 in
                        -h | --help )           restartbibboxusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.restartBibbox()'
        fi

        if [[ $1 = stopSystem ]]
        then

                case $2 in
                        -h | --help )           stopbibboxusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.stopBibbox()'
        fi
}

#function bibbox() 
# {       
#        var1=$1
#
#        case $var1 in
#                -h | --help )           usage
#                                        return
#                                        ;;
#                -v | --version | version )  version
#                                        return
#                                        
#        esac
#        shift
#}

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
    echo "bibbox-startSystem"
    
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
    echo "bibbox-stopSystem"
    
    
}

function restartbibboxusage()
{

    echo "DESCRIPTION"
    echo "Restarts the main bibbox system"
    echo ""
    echo "SYNTAX"
    echo "bibbox-stopBibbox"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox-restartSystem"
    
    
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
