import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {of} from 'rxjs';
import {ApplicationService} from '../services/application.service';
import {
  ApplicationGroupActionTypes,
  LoadApplicationGroupAction, LoadApplicationGroupFailureAction, LoadApplicationGroupSuccessAction
} from '../actions/applications.actions';

@Injectable()
export class ApplicationsEffects {

  loadApplicationGroups$ =  createEffect(() =>
    this.actions$.pipe(
      ofType<LoadApplicationGroupAction>(ApplicationGroupActionTypes.LOAD_APPLICATION_GROUP),
      mergeMap(
        () => this.applicationService.loadApplications()
          .pipe(
            map(data => new LoadApplicationGroupSuccessAction(data)),
            catchError(error => of(new LoadApplicationGroupFailureAction(error)))
          )
      )
    )
  );

  constructor(private actions$: Actions, private applicationService: ApplicationService) {
  }

}
