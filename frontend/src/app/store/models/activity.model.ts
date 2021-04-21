export interface ActivityItem {
  id: number;
  name: string;
  type: string;
  start_time: string;
  finished_time: string | undefined;
  state: string;
  result: string | undefined;
}

export interface LogItem {
  id: number;
  timestamp: string;
  message: string;
  type: string;
  activity_id: number;
}
