import {InstanceState} from '../reducers/instance.reducer';
import {ApplicationGroupState} from '../reducers/application-group.reducer';
import {AuthState} from '../reducers/auth.reducer';
import {ActivityState} from '../reducers/activity.reducer';

export interface AppState {
  instances: InstanceState;
  applicationGroups: ApplicationGroupState;
  activities: ActivityState;
  auth: AuthState;
}
