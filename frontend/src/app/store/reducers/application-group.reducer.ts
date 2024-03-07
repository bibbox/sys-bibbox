import {ApplicationGroupItem, IApplicationGroupsFilters} from '../models/application-group-item.model';
import {ApplicationGroupsAction, ApplicationGroupsActionTypes} from '../actions/applications.actions';
import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

export interface ApplicationGroupState extends EntityState<ApplicationGroupItem> {
  loading: boolean;
  error: Error;
  filters: IApplicationGroupsFilters;
}

export const ApplicationGroupAdapter: EntityAdapter<ApplicationGroupItem> = createEntityAdapter<ApplicationGroupItem>({
  selectId: (a: ApplicationGroupItem) => a.group_name,
});

const defaultState: ApplicationGroupState = {
  ids: [],
  entities: {},
  loading: false,
  error: undefined,
  filters: {
    searchterm: '',
    filter: '',
    sort: 'category'
  }
};

export const initialState = ApplicationGroupAdapter.getInitialState(defaultState);

export const getApplicationGroupsFilters = (state: ApplicationGroupState): IApplicationGroupsFilters => state.filters;

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
      return ApplicationGroupAdapter.upsertMany(action.payload, {
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
    case ApplicationGroupsActionTypes.FILTER_APPLICATION_GROUPS:
      return {
        ...state
      };
    case ApplicationGroupsActionTypes.UPDATE_APPLICATION_GROUPS_FILTERS:
      return {
        ...state,
        filters: action.payload
      };
    default:
      return {...state};
  }
}

// export const applicationGroupReducer = createReducer(
//   initialState,
//   on(LoadApplicationGroupsAction, state => ({...state, loading: true})),
// );
