import {InstanceState} from '../reducers/instance.reducer';
import {ApplicationGroupState} from '../reducers/application-group.reducer';
import {AuthState} from '../reducers/auth.reducer';

export interface AppState {
  instances: InstanceState;
  applicationGroups: ApplicationGroupState;
  auth: AuthState;
}
