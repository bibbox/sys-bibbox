import {InstanceState} from '../reducers/instance.reducer';
import {ApplicationGroupState} from '../reducers/application-group.reducer';
import {AuthState} from '../reducers/auth.reducer';

export interface AppState {
  readonly instances: InstanceState;
  readonly applicationGroups: ApplicationGroupState;
  readonly auth: AuthState;
}
