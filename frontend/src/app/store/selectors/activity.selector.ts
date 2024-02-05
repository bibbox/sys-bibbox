import {createFeatureSelector, createSelector} from '@ngrx/store';
import * as fromActivity from '../reducers/activity.reducer';

const selectActivityState = createFeatureSelector<fromActivity.ActivityState>('activities');

export const selectActivityEntities = createSelector(
  selectActivityState,
  fromActivity.selectActivityEntities,
);

export const selectAllActivities = createSelector(
  selectActivityState,
  fromActivity.selectAllActivities
);

export const selectCurrentActivity = createSelector(
  selectActivityEntities,
  (activityEntities, activityId: number) => {
    return activityEntities[activityId];
  }
);

export const selectActivityFilters = createSelector(
  selectActivityState,
  fromActivity.getActivityFilters
);
