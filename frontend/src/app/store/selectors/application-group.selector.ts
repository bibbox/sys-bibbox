import {createFeatureSelector, createSelector} from '@ngrx/store';
import {ApplicationGroupAdapter, ApplicationGroupState, getApplicationGroupsFilters} from '../reducers/application-group.reducer';

const getApplicationGroupFeatureState = createFeatureSelector<ApplicationGroupState>('applicationGroups');

export const loadApplicationGroups = createSelector(
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

export const selectApplicationGroupsFilters = createSelector(
  getApplicationGroupFeatureState,
  getApplicationGroupsFilters
);
