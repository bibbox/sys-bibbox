export interface InstanceItem {
  instancename: string;
  displayname_short: string;
  displayname_long: string;
  description_short: string;
  description_long: string;
  container_names?: string[];
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
