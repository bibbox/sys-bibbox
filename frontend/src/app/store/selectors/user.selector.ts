import {createFeatureSelector, createSelector} from '@ngrx/store';
import * as fromUser from '../reducers/user.reducer';

const selectUserState = createFeatureSelector<fromUser.UserState>('users');


export const selectUserIds = createSelector(
  selectUserState,
  fromUser.selectAllUsers
);

export const selectUserEntities = createSelector(
  selectUserState,
  fromUser.selectUserEntities,
);

export const selectAllUsers = createSelector(
  selectUserState,
  fromUser.selectAllUsers
);

export const selectUserTotal = createSelector(
  selectUserState,
  fromUser.selectUserTotal
);
//
// export const selectCurrentUserId = createSelector(
//   selectUserState,
//   fromUser.getSelectedUserId
// );

// export const selectCurrentUser = createSelector(
//   selectUserEntities,
//   (userEntities, userId: string) => {
//     return userEntities[userId];
//   }
// );
