import {InstanceState} from '../reducers/instance.reducer';
import {ApplicationGroupState} from '../reducers/application.reducer';

export interface AppState {
  readonly instances: InstanceState;
  readonly applications: ApplicationGroupState;
}
