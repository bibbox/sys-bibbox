export interface ActivityItem {
  id: number;
  instance_uuid: string;
  name: string;
  type_: string;
  start_time: string;
  finished_time: string[];
  state: string;
  result: string;
}
