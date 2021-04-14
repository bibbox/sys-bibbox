export interface InstanceItem {
  instancename: string;
  displayname: string;
  short_description?: string;
  long_description?: string;
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
