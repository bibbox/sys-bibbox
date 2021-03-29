import {InstanceState} from '../reducers/instance.reducer';
import {ApplicationGroupState} from '../reducers/application.reducer';
import {AuthState} from '../reducers/auth.reducer';

export interface AppState {
  readonly instances: InstanceState;
  readonly applications: ApplicationGroupState;
  readonly auth: AuthState;
}
