import {ApplicationGroupItem} from '../models/application-group-item.model';
import {ApplicationGroupAction, ApplicationGroupActionTypes} from '../actions/applications.actions';

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
  state: ApplicationGroupState= initialState,
  action: ApplicationGroupAction
): any {
  switch (action.type) {
    case ApplicationGroupActionTypes.ADD_APPLICATION_GROUP:
      return {...state, ...action.payload};
    case ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP:
      return {
        ...state,
        loading: true
      };
    case ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP_SUCCESS:
      return {
        ...state,
        list: action.payload,
        loading: false
      };
    case ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP_FAILURE:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    default:
      return {...state};
  }
}
