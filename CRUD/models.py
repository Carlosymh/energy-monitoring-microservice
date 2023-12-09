from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

class Dispositivo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_equipo = models.CharField(max_length=255)
    tipodispositivoId = models.ForeignKey('TiposDispositivo', on_delete=models.CASCADE)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    potencia_actual = models.FloatField()
    statusDispositivoId = models.ForeignKey('StatusDispositivo', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):

        if self.potencia_actual < 0:
            raise ValidationError("La potencia actual no puede ser un número negativo.")
        
        if not TiposDispositivo.objects.filter(id=self.tipodispositivoId.id).exists():
            raise ValidationError("El TipoDispositivoId no existe.")

        if not StatusDispositivo.objects.filter(id=self.statusDispositivoId.id).exists():
            raise ValidationError("El StatusDispositivoId no existe.")
        
        
        is_new_device = self._state.adding
        if is_new_device:
            if self.statusDispositivoId.descripcion == 'En mantenimiento' and self.potencia_actual > 0:
                raise ValidationError("No se puede registrar la potencia actual si en Dispositivo esta en mantenimiento.")
        


        super().save(*args, **kwargs)

        if is_new_device:
            
            if self.statusDispositivoId.descripcion == 'En mantenimiento':
                Mantenimientos.objects.create(iddispositivo=self, fecha_ingreso_mantenimiento=self.fecha_actualizacion)
            else:
                Lecturas.objects.create(
                    iddispositivo=self,
                    idtipodispositivo=self.tipodispositivoId,
                    potenciaActual=self.potencia_actual
                )
        else:
            if self.statusDispositivoId.descripcion == 'En mantenimiento':
                Mantenimientos.objects.create(iddispositivo=self, fecha_ingreso_mantenimiento=self.fecha_actualizacion)

            elif self.statusDispositivoId.descripcion == 'En operación':
                try:
                    ultimo_mantenimiento = Mantenimientos.objects.filter(iddispositivo=self).latest('fecha_ingreso_mantenimiento')
                    ultimo_mantenimiento.fecha_salida_mantenimiento = self.fecha_actualizacion
                    ultimo_mantenimiento.save()
                except Mantenimientos.DoesNotExist:
                    pass  

  

class TiposDispositivo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=255)

class StatusDispositivo(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)


class Lecturas(models.Model):
    id = models.AutoField(primary_key=True)
    iddispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    idtipodispositivo = models.ForeignKey('TiposDispositivo', on_delete=models.CASCADE)
    potenciaActual = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.potenciaActual < 0:
            raise ValidationError("La potencia actual no puede ser un número negativo.")
        
        if self.iddispositivo.statusDispositivoId.descripcion == 'En mantenimiento':
            raise ValidationError("No se puede registrar una lectura para un dispositivo en mantenimiento.")
        

        super().save(*args, **kwargs)

@receiver(pre_save, sender=Lecturas)
def validar_tipoystatus_existen(sender, instance, **kwargs):

    if not Dispositivo.objects.filter(id=instance.iddispositivo.id).exists():
        raise ValidationError("El iddispositivo no existe.")

    if not TiposDispositivo.objects.filter(id=instance.idtipodispositivo.id).exists():
        raise ValidationError("El idtipodispositivo no existe.")
    

@receiver(post_save, sender=Lecturas)
def validar_tipoystatus_existen(sender, instance, **kwargs):
    
    dispositivo = Dispositivo.objects.get(id=instance.iddispositivo.id)
    dispositivo.potencia_actual = instance.potenciaActual
    dispositivo.fecha_actualizacion = instance.timestamp
    dispositivo.save()

class Mantenimientos(models.Model):
    id = models.AutoField(primary_key=True)
    iddispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    fecha_ingreso_mantenimiento = models.DateTimeField(auto_now_add=True)
    fecha_salida_mantenimiento = models.DateTimeField(default=timezone.now, null=True, blank=True)

@receiver(pre_save, sender=Mantenimientos)
def validar_dispositivo_existen(sender, instance, **kwargs):
    
    if not Dispositivo.objects.filter(id=instance.iddispositivo.id).exists():
        raise ValidationError("El DispositivoId no existe.")
