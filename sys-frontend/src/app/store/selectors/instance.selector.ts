import {createFeatureSelector, createSelector} from '@ngrx/store';
import {InstanceAdapter, InstanceState} from '../reducers/instance.reducer';

const getInstanceFeatureState = createFeatureSelector<InstanceState>('instances');

export const loadInstances = createSelector(
  getInstanceFeatureState,
  InstanceAdapter.getSelectors().selectAll
);

export const getInstancesLoading = createSelector(
  getInstanceFeatureState,
  (state: InstanceState) => state.loading
);

export const getInstancesError = createSelector(
  getInstanceFeatureState,
  (state: InstanceState) => state.error
);

export const getCurrentInstanceID = createSelector(
  getInstanceFeatureState,
  (state: InstanceState) => state.selectedEntityID
);

export const getCurrentInstance = createSelector(
  getInstanceFeatureState,
  getCurrentInstanceID,
  state => state.entities[state.selectedEntityID]
);
