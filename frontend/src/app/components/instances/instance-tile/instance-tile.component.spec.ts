import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstanceTileComponent } from './instance-tile.component';

describe('InstanceTileComponent', () => {
  let component: InstanceTileComponent;
  let fixture: ComponentFixture<InstanceTileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstanceTileComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstanceTileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
