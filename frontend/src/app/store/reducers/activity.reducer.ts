import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';
import {ActivityItem, IActivityFilters} from '../models/activity.model';
import {ActivityAction, ActivityActionTypes} from '../actions/activity.actions';

export interface ActivityState extends EntityState<ActivityItem>{
  selectedEntityID: number;
  loading: boolean;
  error: Error;
  filters: IActivityFilters;
}

export const ActivityAdapter: EntityAdapter<ActivityItem> = createEntityAdapter<ActivityItem>();

const defaultState: ActivityState = {
  ids: [],
  entities: {},
  selectedEntityID: null,
  loading: false,
  error: undefined,
  filters: {
    searchterm: '',
    state: '',
    type: ''
  }
};

export const initialState = ActivityAdapter.getInitialState(defaultState);

export const getActivityFilters = (state: ActivityState): IActivityFilters => state.filters;

export function ActivityReducer(
  state: ActivityState = defaultState,
  action: ActivityAction
): any {
  switch (action.type) {
    case ActivityActionTypes.LOAD_ACTIVITIES:
      return {
        ...state,
        loading: true
      };
    case ActivityActionTypes.LOAD_ACTIVITIES_SUCCESS:
      return ActivityAdapter.upsertMany(action.payload, {
        ...state,
        loading: false,
        error: undefined
      });
    case ActivityActionTypes.LOAD_ACTIVITIES_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    case ActivityActionTypes.UPDATE_ACTIVITIES_FILTERS:
      return {
        ...state,
        filters: action.payload
      };
    default:
      return {...state};
  }
}

export const {
  selectAll: selectAllActivities,
  selectEntities: selectActivityEntities,
} = ActivityAdapter.getSelectors();
