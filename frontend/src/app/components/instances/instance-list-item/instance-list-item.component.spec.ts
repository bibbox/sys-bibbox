import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstanceListItemComponent } from './instance-list-item.component';

describe('InstanceTileComponent', () => {
  let component: InstanceListItemComponent;
  let fixture: ComponentFixture<InstanceListItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstanceListItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstanceListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
