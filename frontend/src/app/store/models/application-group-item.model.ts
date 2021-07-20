import {EntityState} from '@ngrx/entity';

export interface ApplicationGroupItem {
  group_name: string;
  group_members: ApplicationItem[];
}

export interface ApplicationItem {
  app_name: string;
  app_display_name: string;
  short_description: string;
  installable: boolean;
  decoration: string;
  tags: string[];
  versions: IVersions[];
  icon_url: string;
}

export interface IVersions {
  app_version: string;
  version: string;
  tooltip: string;
  appinfo: string;
  environment_parameters: string;
}

export interface AppInfo {
  name: string;
  short_name: string;
  version: string;
  description: string;
  short_description: string;
  catalog_url: string;
  application_url: string;
  tags: string[];
  application_documentation_url: string;
}

export interface EnvironmentParameters {
  id: string;
  display_name: string;
  type: string;
  default_value: string;
  description: string;
  min_length: string;
  max_length: string;
}
