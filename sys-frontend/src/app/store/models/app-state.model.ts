import {InstanceItem} from './instance-item.model';
import {ApplicationGroupItem} from './application-group-item.model';

export interface AppState {
  readonly instance: Array<InstanceItem>;
  readonly applications: Array<ApplicationGroupItem>;
}
