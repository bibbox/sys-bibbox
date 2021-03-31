import {ApplicationGroupItem} from '../models/application-group-item.model';
import {ApplicationGroupsAction, ApplicationGroupsActionTypes} from '../actions/applications.actions';

export interface ApplicationGroupState {
  list: ApplicationGroupItem[];
  loading: boolean;
  error: Error;
}

const initialState: ApplicationGroupState = {
  list: [],
  loading: false,
  error: undefined
};

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
      return {
        ...state,
        list: action.payload,
        loading: false,
        error: undefined
      };
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
