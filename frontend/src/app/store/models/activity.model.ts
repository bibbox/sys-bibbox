export interface ActivityItem {
  id: number;
  name: string;
  type: string;
  start_time: string;
  finished_time: string | undefined;
  state: string;
  result: string | undefined;
  user?: {
    id: string | null;
    username: string | null;
    firstName: string | null;
    lastName: string | null;
  }
}

export interface LogItem {
  id: number;
  timestamp: string;
  message: string;
  type: string;
  activity_id: number;
}

export interface SysContainerNames {
  names: string[];
}

export interface SysContainerLogs {
  name: string,
  tail: number,
  logs: string[];
}

export interface IActivityFilters {
  searchterm: string;
  state: string;
  type: string;
}
