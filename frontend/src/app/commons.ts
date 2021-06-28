// strings


export const APP_TITLE_LONG = 'Silicolab Bibbox v4.0';
export const APP_TITLE_SHORT = 'Bibbox v4.0';


export const API_INSTANCES_URL = '/api/v1/instances/';
export const API_APPLICATIONS_URL = '/api/v1/apps/';
export const API_ACTIVITY_URL = '/api/v1/activities/';
export const API_AUTH_URL = '/api/v1/users/';

export const SOCKET_IO_URL = '/socketio';


export const  SVG_PATHS = {
  start: 'M451.523,528.59V47.615c0-26.233,21.267-47.5,47.5-47.5s47.5,21.267,47.5,47.5V528.59c0,26.233-21.267,47.5-47.5,47.5S451.523,554.823,451.523,528.59z M711.563,158.396c-23.034-12.554-51.885-4.056-64.438,18.98s-4.055,51.885,18.98,64.438c113.472,61.835,183.962,180.438,183.962,309.526c0,94.084-36.639,182.536-103.165,249.063c-66.527,66.527-154.979,103.166-249.063,103.166s-182.537-36.639-249.064-103.166S145.609,645.424,145.609,551.34c0-129.281,70.646-247.969,184.369-309.747c23.052-12.522,31.587-41.361,19.065-64.413c-12.522-23.052-41.362-31.586-64.413-19.065C140.281,236.53,50.609,387.206,50.609,551.34c0,60.354,11.831,118.929,35.165,174.097c22.528,53.261,54.769,101.085,95.826,142.143c41.057,41.057,88.881,73.298,142.143,95.825c55.167,23.334,113.742,35.165,174.097,35.165s118.93-11.831,174.097-35.165c53.261-22.527,101.085-54.769,142.142-95.826c41.058-41.057,73.298-88.881,95.825-142.143c23.334-55.167,35.165-113.741,35.165-174.096C945.068,387.45,855.595,236.883,711.563,158.396z',
  stop: 'M451.523,528.59V47.615c0-26.233,21.267-47.5,47.5-47.5s47.5,21.267,47.5,47.5V528.59c0,26.233-21.267,47.5-47.5,47.5S451.523,554.823,451.523,528.59z M711.563,158.396c-23.034-12.554-51.885-4.056-64.438,18.98s-4.055,51.885,18.98,64.438c113.472,61.835,183.962,180.438,183.962,309.526c0,94.084-36.639,182.536-103.165,249.063c-66.527,66.527-154.979,103.166-249.063,103.166s-182.537-36.639-249.064-103.166S145.609,645.424,145.609,551.34c0-129.281,70.646-247.969,184.369-309.747c23.052-12.522,31.587-41.361,19.065-64.413c-12.522-23.052-41.362-31.586-64.413-19.065C140.281,236.53,50.609,387.206,50.609,551.34c0,60.354,11.831,118.929,35.165,174.097c22.528,53.261,54.769,101.085,95.826,142.143c41.057,41.057,88.881,73.298,142.143,95.825c55.167,23.334,113.742,35.165,174.097,35.165s118.93-11.831,174.097-35.165c53.261-22.527,101.085-54.769,142.142-95.826c41.058-41.057,73.298-88.881,95.825-142.143c23.334-55.167,35.165-113.741,35.165-174.096C945.068,387.45,855.595,236.883,711.563,158.396z',
  restart: 'M992.001,507.999c0,66.4-13.015,130.838-38.683,191.522c-24.782,58.593-60.251,111.205-105.421,156.375s-97.782,80.639-156.375,105.421C630.838,986.985,566.4,1000,500,1000s-130.838-13.015-191.523-38.683c-58.592-24.782-111.204-60.251-156.373-105.421c-45.171-45.17-80.64-97.782-105.422-156.375C21.014,638.837,7.999,574.399,7.999,507.999c0-94.006,26.612-185.405,76.962-264.315c32.16-50.405,72.985-94.28,120.361-129.74l-65.975-97.322L459.096,0L325.479,291.191l-69.749-102.89c-37.34,28.562-69.592,63.569-95.152,103.63c-41.137,64.473-62.881,139.188-62.881,216.068c0,107.459,41.848,208.486,117.832,284.471C291.514,868.455,392.541,910.302,500,910.302s208.486-41.847,284.471-117.832c75.985-75.984,117.831-177.012,117.831-284.471c0-65.419-16.042-130.34-46.392-187.744c-29.407-55.622-72.15-104.294-123.606-140.756c-20.21-14.321-24.983-42.314-10.663-62.524c14.321-20.21,42.315-24.984,62.524-10.664c62.867,44.548,115.097,104.031,151.042,172.018C972.361,348.603,992.001,428.021,992.001,507.999z',
  install: 'M1000,937.667c0,33.138-26.864,60.002-60.002,60.002H60.003C26.864,997.669,0,970.805,0,937.667c0-33.139,26.864-60.003,60.003-60.003h879.995C973.136,877.664,1000,904.528,1000,937.667z M500,817.443l273.352-273.285H575.003V75.003C575.003,33.58,541.423,0,500,0c-41.423,0-75.003,33.58-75.003,75.003v469.155H226.648L500,817.443z',
  delete: 'M861.436,120.218c0,23.419-18.73,42.154-42.149,42.154H180.718c-23.419,0-42.153-18.734-42.153-42.154s18.734-42.154,42.153-42.154h238.097C420.373,35.129,456.283,0,500,0c43.713,0,79.627,35.129,81.189,78.846h238.097C842.705,78.846,861.436,97.58,861.436,120.218z M838.017,222.483c7.807,8.588,11.71,20.298,10.932,32.007l-55.43,706.479c-1.556,21.863-20.294,39.031-42.15,39.031H248.632c-21.856,0-39.81-17.168-42.154-39.031L151.052,254.49c-0.778-11.709,3.125-23.419,10.932-32.007c7.807-8.587,19.517-13.272,31.226-13.272h613.582C818.501,209.21,829.433,213.896,838.017,222.483z M357.145,925.062l-45.28-608.902c-0.781-11.709-10.928-20.297-22.638-19.516c-11.709,0.782-20.297,10.928-19.516,22.638l45.275,608.905c0.781,10.924,10.15,19.516,21.079,19.516c0.781,0,0.781,0,1.562,0C349.338,946.141,357.922,936.771,357.145,925.062z M521.856,317.723c0-11.71-9.369-21.079-21.075-21.079c-11.71,0-21.079,9.369-21.079,21.079v608.902c0,11.709,9.369,21.078,21.079,21.078c11.706,0,21.075-9.369,21.075-21.078V317.723z M731.067,319.282c0.785-11.71-7.807-21.856-19.517-22.638c-11.709-0.781-21.856,7.807-22.634,19.516l-45.275,608.902c-0.785,11.709,7.806,21.855,19.516,22.641c0.777,0,0.777,0,1.556,0c10.932,0,20.301-8.592,21.078-19.516L731.067,319.282z',
};


// proxy.conf.json
// "/socket.io": {
//     "target": "http://localhost:5000/socket.io", // "http://silicolabv4.bibboxlocal/socket.io",
//     "secure": false,
//     "changeOrigin": true,
//     "ws": true,
//     "logLevel": "debug"
//   }
