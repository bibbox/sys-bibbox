import {ApplicationGroupItem} from '../models/application-group-item.model';
import {ApplicationGroupAction, ApplicationGroupActionTypes} from '../actions/applications.actions';

const initialState: Array<ApplicationGroupItem> = [];

export function ApplicationGroupReducer(
  state: Array<ApplicationGroupItem> = initialState,
  action: ApplicationGroupAction
): any {
  switch (action.type) {
    case ApplicationGroupActionTypes.ADD_APPLICATION_GROUP:
      return [...state, action.payload];
    default:
      return [...state];
  }
}
