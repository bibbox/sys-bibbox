// import {Injectable} from '@angular/core';
// import {Actions, createEffect, ofType, Effect} from '@ngrx/effects';
// import {InstanceActionTypes, LoadInstanceAction, LoadInstanceSuccessAction} from '../actions/instance.actions';
// import {map, mergeMap} from 'rxjs/operators';
// import {InstanceService} from '../../app/utils/instance.service';
// import {InstanceItem} from '../models/instance-item.model';
//
// @Injectable()
// export class InstanceEffects {
//
//   @Effect() loadInstances$ = this.actions$
//     .pipe(
//       ofType<LoadInstanceAction>(InstanceActionTypes.LOAD_INSTANCES),
//       mergeMap(
//         () => this.instanceService.getAllInstances()
//           .pipe(
//             map(data => new LoadInstanceSuccessAction(data))
//           )
//       )
//     )
//
//   constructor(private actions$: Actions, private instanceService: InstanceService) {
//
//   }
//
// }
