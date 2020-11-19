
#!/bin/bash

function bibbox() 
{       
        if [[ $1 = install ]]
        then
                appname="'$2'"
                appnamech=$2
                instance="'$3'"
                instancech=$3
                #version="'$4'"
                #versionch=$4
                default=false
                paramsset=false
                
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
                                                        
                                                        ;;
                                -p | --params )         paramlistset=$4 
                                                        echo $paramlistset   
                                                        paramsset=true     
                                
                        esac
                        shift
                        

                done
                
                
                declare name
                name=$(sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.getAppName('"$appname"')' 2>&1)
                declare keylist
                declare paramlist

                if [ -z ${version+y} ]; then
                        echo No parameter for version got set!
                        echo Installing the default version.
                        declare x
                        x=$(git ls-remote --heads https://github.com/bibbox/${name})
                        branches=()
                        for word in $x
                                do
                                word=${word##*/}
                                if [[ $word == *_tng ]]
                                then 
                                branch=${word#"refs/heads/"}
                                branches+=($branch)
                                fi
                        done

                        sorted=$(echo ${branches[*]} | tr ' ' '\n' | sort --version-sort --field-separator=- -r)

                        sortedlist=($sorted)

                        newest=${sortedlist[0]}
                        version="'$newest'"
                        versionch=$newest
                        echo Latest version is: $newest
                fi


                params=$(curl https://raw.githubusercontent.com/bibbox/"${name}"/"$versionch"/.env)
                sed -n s/' '/'='/g <<< $params
                echo https://raw.githubusercontent.com/bibbox/${name}/$versionch/.env
                
                echo The user specifications are used for the login later.
                #ext = begin
                keylist="'"
                paramlist="'"
                if [ $paramsset = 'false' ]
                then
                        if [ $default = 'false' ]
                        then
                                echo Please enter user specifications!
                        fi

                        if [ $default = 'true' ]
                        then
                                echo The selected default values are:
                        fi
                fi
                if [ $paramsset = 'true' ]
                then
                        echo Parameters set by flag
                fi

                for item in $params
                do
        
                IFS='='
                read -a strarr <<< $item
                IFS=$'\n'
                read -a out <<< $item
                if [ ${strarr[0]} != 'PORT' ] && [ ${strarr[0]} != 'INSTANCE' ] 
                then
                        if [ $paramsset = 'false' ]
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
                        if [ $paramsset = 'true' ]
                        then
                                v1=${strarr[0]}
                                keylist="$keylist;$v1"
                                paramlist="'$paramlistset'"
                        fi
                fi        
                done
                keylist="$keylist'"
                paramlist="$paramlist'"
                if [ $paramsset = 'true' ]
                then
                        paramlist="';$paramlistset'"
                fi
                
                sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.installApp('"$paramlist"','"$keylist"','"$instance"','"$appname"','"$version"',CLI=True)'
                unset paramlist keylist instance instancech appname version versionch name word x branch branches

        fi

        if [[ $1 = info ]]
        then
                appname="'$2'"
                appnamech=$2
                
                case $2 in
                        -h | --help )           infousage
                                                return
                                                ;;
                        -bv | --bibboxversion )  version
                                                return
                                                      
                esac
                
                declare name
                name=$(sudo python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.getAppName('"$appname"')' 2>&1)
                declare keylist
                declare paramlist

                declare x
                x=$(git ls-remote --heads https://github.com/bibbox/${name})
                branches=()
                for word in $x
                        do
                        word=${word##*/}
                        if [[ $word == *_tng ]]
                        then 
                        branch=${word#"refs/heads/"}
                        branches+=($branch)
                        fi
                done

                sorted=$(echo ${branches[*]} | tr ' ' '\n' | sort --version-sort --field-separator=- -r)

                sortedlist=($sorted)

                newest=${sortedlist[0]}
                version="'$newest'"
                versionch=$newest
        
                params=$(curl https://raw.githubusercontent.com/bibbox/"${name}"/"$versionch"/.env)
                sed -n s/' '/'='/g <<< $params
                echo https://raw.githubusercontent.com/bibbox/${name}/$versionch/.env
                
                keylist="'"
                paramlist="'"
                echo
                echo The default parameters are:

                for item in $params
                do
        
                IFS='='
                read -a strarr <<< $item
                IFS=$'\n'
                read -a out <<< $item
                if [ ${strarr[0]} != 'PORT' ] && [ ${strarr[0]} != 'INSTANCE' ] 
                then
                
                echo ${strarr[0]}:  '('default = ${strarr[1]}')'
                        
                fi        
                done
                echo
                echo The app specifications are:
                echo Repository name: ${name}
                echo Available versions:
                echo ${branches[*]}

                unset paramlist keylist instance instancech appname version versionch name word x branch branches
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

        if [[ $1 = listInstances ]]
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

        if [[ $1 = checkSystem ]]
        then

                case $2 in
                        -h | --help )           checkbibboxusage
                                                return
                                                ;;
                        -v | --version | version )  version
                                                return
                                                
                esac
                shift

                echo Checking requirements!
                
                python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.checkSystem()'
                state=$(python3 -c 'import sys; sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend"); import mainFunctions; x=mainFunctions.MainFunctions(); x.checkProxy("local_nginx")' 2>&1)
                echo $state

        fi


   
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
    echo "Installs a new Bibbox app with a specific unique name"
    echo ""
    echo "SYNTAX"
    echo "bibbox install <appname> -n <instancename> -v <version> -p <paarameters>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-bv, --bibboxversion          Print script information"
    echo "-n, --name                    Specify the name of the installed instance. The instance name can also be set without flag as the second function argument."
    echo "-v, --version                 Specify the app version you want to install. This flag is optional. If not specified, the newest version gets installed."
    echo "-p, --params                  The app parameters can be passed to this function automatically. This flag is optional. If not specified, the app parameters can be set to default or set interactively."
    echo "-d, --default                 If this flag is set, the default app parameters are used for installation."
    echo ""
    echo "EXAMPLES"
    echo "bibbox install nextcloud -n mynextcloud -v v20-0-x_tng -p 'nextcloud,nextcloud'"
    echo "bibbox install nextcloud -n mynextcloud -d"
    echo "bibbox install nextcloud mynextcloud"
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
    echo "Starts the wanted Bibbox app container"
    echo ""
    echo "SYNTAX"
    echo "bibbox start <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox start seeddmstest"
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
    echo "Stops the wanted Bibbox app container"
    echo ""
    echo "SYNTAX"
    echo "bibbox stop <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox stop seeddmstest"
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
    echo "Removes the wanted Bibbox app container"
    echo ""
    echo "SYNTAX"
    echo "bibbox remove <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox remove seeddmstest"
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
    echo "bibbox status <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox status seeddmstest"
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
    echo "bibbox copy <instancename>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox copy oldappname newappname"
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
    echo "Lists all available applications"
    echo ""
    echo "SYNTAX"
    echo "bibbox listApps"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox listApps"
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
    echo "bibbox listInstances"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox listInstances"
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
    echo "Starts the main Bibbox system"
    echo ""
    echo "SYNTAX"
    echo "bibbox startSystem"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox startSystem"
    
}

function stopbibboxusage()
{

    echo "DESCRIPTION"
    echo "Stops the main Bibbox system"
    echo ""
    echo "SYNTAX"
    echo "bibbox stopSystem"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox stopSystem"
    
    
}

function restartbibboxusage()
{

    echo "DESCRIPTION"
    echo "Restarts the main Bibbox system"
    echo ""
    echo "SYNTAX"
    echo "bibbox restartSystem"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox restartSystem"
    
    
}

function infousage()
{

    echo "DESCRIPTION"
    echo "Returns install information about a specific application. This information contains the available versions, the input parameters etc."
    echo ""
    echo "SYNTAX"
    echo "bibbox info <appname>"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    echo "EXAMPLES"
    echo "bibbox info seeddms"
    
    
}


function checkbibboxusage()
{

    echo "DESCRIPTION"
    echo "Performs System Check. Checks if all required services are running and controls the versions of the used packages."
    echo ""
    echo "SYNTAX"
    echo "bibbox checkSystem"
    echo ""
    echo "OPTIONS"
    echo "-h, --help                    Print this help"
    echo "-v, --version                 Print script information"
    echo ""
    
    
}

function usage()
{

    echo "DESCRIPTION"
    echo "This module is made to controll the BiBBoX software through a CLI."
    echo "The following functiuons are available:"
    echo "bibbox install"
    echo "bibbox start"
    echo "bibbox stop"
    echo "bibbox copy"
    echo "bibbox listApps"
    echo "bibbox listInstances"
    echo "bibbox remove"
    echo "bibbox status"
    echo "bibbox startSystem"
    echo "bibbox stopSystem"
    echo "bibbox restartSystem"
    echo "bibbox info"
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
