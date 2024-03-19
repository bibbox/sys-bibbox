import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstanceDeleteDialogComponent } from './instance-delete-dialog.component';

describe('InstanceDeleteDialogComponent', () => {
  let component: InstanceDeleteDialogComponent;
  let fixture: ComponentFixture<InstanceDeleteDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstanceDeleteDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstanceDeleteDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
