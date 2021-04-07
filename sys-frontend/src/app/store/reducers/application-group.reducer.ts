import {ApplicationGroupItem} from '../models/application-group-item.model';
import {ApplicationGroupsAction, ApplicationGroupsActionTypes} from '../actions/applications.actions';
import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';
import {createFeatureSelector, createSelector} from '@ngrx/store';

export interface ApplicationGroupState extends EntityState<ApplicationGroupItem>{
  selectedEntityID: number | null;
  loading: boolean;
  error: Error;
}

export const ApplicationGroupAdapter: EntityAdapter<ApplicationGroupItem> = createEntityAdapter<ApplicationGroupItem>({
  selectId: (a: ApplicationGroupItem) => a.group_name,
});

const defaultState: ApplicationGroupState = {
  ids: [],
  entities: {},
  selectedEntityID: null,
  loading: false,
  error: undefined
};

export const initialState = ApplicationGroupAdapter.getInitialState(defaultState);

export function ApplicationGroupReducer(
  state: ApplicationGroupState = initialState,
  action: ApplicationGroupsAction
): any {
  switch (action.type) {
    case ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS:
      return {
        ...state,
        loading: true
      };
    case ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS_SUCCESS:
      return ApplicationGroupAdapter.addMany(action.payload, {
          ...state,
          loading: false,
          error: undefined
        });
    case ApplicationGroupsActionTypes.LOAD_APPLICATION_GROUPS_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    default:
      return {...state};
  }
}
const getApplicationGroupFeatureState = createFeatureSelector<ApplicationGroupState>('applicationGroups');

export const loadApplications = createSelector(
  getApplicationGroupFeatureState,
  ApplicationGroupAdapter.getSelectors().selectAll
);

export const getApplicationGroupsLoading = createSelector(
  getApplicationGroupFeatureState,
  (state: ApplicationGroupState) => state.loading
);


export const getApplicationGroupsError = createSelector(
  getApplicationGroupFeatureState,
  (state: ApplicationGroupState) => state.error
);

export const getCurrentApplicationGroupID = createSelector(
  getApplicationGroupFeatureState,
  (state: ApplicationGroupState) => state.selectedEntityID
);

export const getCurrentApplicationGroup = createSelector(
  getApplicationGroupFeatureState,
  getCurrentApplicationGroupID,
  state => state.entities[state.selectedEntityID]
);


