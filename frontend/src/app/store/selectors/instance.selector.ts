import {createFeatureSelector, createSelector} from '@ngrx/store';
import * as fromInstance from '../reducers/instance.reducer';

const selectInstanceState = createFeatureSelector<fromInstance.InstanceState>('instances');


export const selectInstanceIds = createSelector(
  selectInstanceState,
  fromInstance.selectInstanceIds
);

export const selectInstanceEntities = createSelector(
  selectInstanceState,
  fromInstance.selectInstanceEntities,
);

export const selectAllInstances = createSelector(
  selectInstanceState,
  fromInstance.selectAllInstances
);

export const selectInstanceTotal = createSelector(
  selectInstanceState,
  fromInstance.selectInstanceTotal
);

export const selectCurrentInstanceId = createSelector(
  selectInstanceState,
  fromInstance.getSelectedInstanceId
);

export const selectCurrentInstance = createSelector(
    selectInstanceEntities,
    (instanceEntities, instanceId: string) => {
      return instanceEntities[instanceId];
    }
);
