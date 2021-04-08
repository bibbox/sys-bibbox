import {ApplicationGroupItem} from '../models/application-group-item.model';
import {ApplicationGroupsAction, ApplicationGroupsActionTypes} from '../actions/applications.actions';
import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

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

// export const applicationGroupReducer = createReducer(
//   initialState,
//   on(LoadApplicationGroupsAction, state => ({...state, loading: true})),
// );



