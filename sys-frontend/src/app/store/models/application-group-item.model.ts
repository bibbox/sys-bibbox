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
  docker_version: string;
  version: string;
  tooltip: string;
  appinfo: string;
  environment_parameters: string;
}
