import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstallScreenComponent } from './install-screen.component';

describe('InstallScreenComponent', () => {
  let component: InstallScreenComponent;
  let fixture: ComponentFixture<InstallScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstallScreenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstallScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
