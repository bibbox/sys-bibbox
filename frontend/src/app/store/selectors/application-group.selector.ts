import {createFeatureSelector, createSelector} from '@ngrx/store';
import {ApplicationGroupAdapter, ApplicationGroupState} from '../reducers/application-group.reducer';

const getApplicationGroupFeatureState = createFeatureSelector<ApplicationGroupState>('applicationGroups');

export const loadApplications = createSelector(
  getApplicationGroupFeatureState,
  ApplicationGroupAdapter.getSelectors().selectAll
);

export const getApplications = createSelector(
  getApplicationGroupFeatureState,
  (state: ApplicationGroupState) => state.entities
);

export const getApplicationGroupsLoading = createSelector(
  getApplicationGroupFeatureState,
  (state: ApplicationGroupState) => state.loading
);

export const getApplicationGroupsError = createSelector(
  getApplicationGroupFeatureState,
  (state: ApplicationGroupState) => state.error
);

// export const getCurrentApplicationGroupID = createSelector(
//   getApplicationGroupFeatureState,
//   (state: ApplicationGroupState) => state.selectedEntityID
// );
//
// export const getCurrentApplicationGroup = createSelector(
//   getApplicationGroupFeatureState,
//   getCurrentApplicationGroupID,
//   state => state.entities[state.selectedEntityID]
// );
