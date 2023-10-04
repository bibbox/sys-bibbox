export interface InstanceGroupItem {
  group_name: string;
  group_members: InstanceItem[];
  hideCategory?: boolean;
}

export interface InstanceItem {
  instancename: string;
  installed_by_id?: string; //currently optional to support old instances
  installed_by_name?: string //currently optional to support old instances
  time_of_installation?: string; //currently optional to support old instances
  last_stop_time?: string;
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
