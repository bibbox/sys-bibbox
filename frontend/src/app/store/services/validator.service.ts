import { Injectable } from '@angular/core';
import {AbstractControl, AsyncValidatorFn, FormGroup, ValidationErrors} from '@angular/forms';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {InstanceService} from './instance.service';

@Injectable({
  providedIn: 'root'
})
export class ValidatorService {

  constructor(private instanceService: InstanceService) { }

  getFormValidationErrors(form: FormGroup): void {

    let totalErrors = 0;

    Object.keys(form.controls).forEach(key => {
      const controlErrors: ValidationErrors = form.get(key).errors;
      if (controlErrors != null) {
        totalErrors++;
        Object.keys(controlErrors).forEach(keyError => {
          console.log('Key control: ' + key + ', keyError: ' + keyError + ', err value: ', controlErrors[keyError]);
        });
      }
    });

    console.warn('Number of errors: ' , totalErrors);
  }

  // Custom Validators -----------------------------------------------------
  noWhitespaceValidator(control: AbstractControl): {[key: string]: any} | null {
    const isSpace = (control.value || '').match(/\s/g);
    return isSpace ? {whitespace: true} : null;
  }
}
