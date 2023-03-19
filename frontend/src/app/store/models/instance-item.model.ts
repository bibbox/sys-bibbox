export interface InstanceItem {
  instancename: string;
  installed_by?: string; //currently optional to support old instances
  displayname_short: string;
  displayname_long: string;
  description_short: string;
  description_long: string;
  container_names: string[];
  icon_url?: string;
  state: string;
  app: IApp;
  proxy: IProxy[];
}

export interface IProxy {
  CONTAINER: string;
  URLPREFIX: string;
  TYPE: string;
  TEMPLATE: string;
  DISPLAYNAME: string;
}

export interface IApp {
  organization: string;
  name: string;
  version: string;
}
