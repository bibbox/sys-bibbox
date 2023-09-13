import {HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {MatSnackBar} from '@angular/material/snack-bar';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import * as jsonErrorMessages from '../assets/errorMessages.json';

export class HttperrorInterceptor implements HttpInterceptor {
  errorMessages: any = jsonErrorMessages;
  constructor(private snackBar: MatSnackBar) {
  }


  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage;
          if (error.error instanceof ErrorEvent) {
            // client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // server-side error

            if (error.status in this.errorMessages){
              //Use user friendly Message if available
              errorMessage = `Error Code: ${error.status}: ${this.errorMessages[error.status]}`;
            }else{
              errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
            }

          }
          this.snackBar.open(errorMessage, 'OK');
          return throwError(errorMessage);
        })
      );
  }
}
