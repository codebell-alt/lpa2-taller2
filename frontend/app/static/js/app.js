// JavaScript para el Generador de Facturas

document.addEventListener('DOMContentLoaded', function() {
    const previewBtn = document.getElementById('previewBtn');
    const previewSection = document.getElementById('previewSection');
    const previewContent = document.getElementById('previewContent');
    const numeroFacturaInput = document.getElementById('numero_factura');

    // Evento para vista previa
    previewBtn.addEventListener('click', function() {
        const numeroFactura = numeroFacturaInput.value.trim();

        if (!numeroFactura) {
            alert('Por favor, ingresa un número de factura');
            numeroFacturaInput.focus();
            return;
        }

        // Mostrar loading
        previewContent.innerHTML = `
            <div class="flex items-center justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                <span class="ml-2 text-gray-600">Cargando vista previa...</span>
            </div>
        `;
        previewSection.classList.remove('hidden');

        // Hacer petición AJAX
        fetch(`/api/factura/${encodeURIComponent(numeroFactura)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Factura no encontrada');
                }
                return response.json();
            })
            .then(data => {
                mostrarPreview(data);
            })
            .catch(error => {
                previewContent.innerHTML = `
                    <div class="text-center py-8">
                        <i class="fas fa-exclamation-triangle text-yellow-500 text-3xl mb-2"></i>
                        <p class="text-gray-600">Error: ${error.message}</p>
                    </div>
                `;
            });
    });

    function mostrarPreview(factura) {
        const itemsHtml = factura.items.map(item => `
            <tr class="border-b border-gray-200">
                <td class="py-2">${item.descripcion}</td>
                <td class="py-2 text-center">${item.cantidad}</td>
                <td class="py-2 text-right">$${item.precio_unitario.toLocaleString('es-CO')} COP</td>
                <td class="py-2 text-right font-medium">$${item.subtotal.toLocaleString('es-CO')} COP</td>
            </tr>
        `).join('');

        previewContent.innerHTML = `
            <div class="space-y-6">
                <!-- Header de la factura -->
                <div class="border-b border-gray-300 pb-4">
                    <h4 class="text-xl font-bold text-gray-900 mb-2">FACTURA ${factura.numero_factura}</h4>
                    <p class="text-sm text-gray-600">Fecha: ${factura.fecha_emision}</p>
                </div>

                <!-- Información del cliente -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <h5 class="font-semibold text-gray-900 mb-2">Cliente</h5>
                        <div class="text-sm text-gray-600 space-y-1">
                            <p><strong>Nombre:</strong> ${factura.cliente_nombre}</p>
                            <p><strong>Email:</strong> ${factura.cliente_email}</p>
                            <p><strong>Teléfono:</strong> ${factura.cliente_telefono}</p>
                            <p><strong>Dirección:</strong> ${factura.cliente_direccion}</p>
                            <p><strong>Ciudad:</strong> ${factura.cliente_ciudad}</p>
                        </div>
                    </div>
                </div>

                <!-- Detalle de items -->
                <div>
                    <h5 class="font-semibold text-gray-900 mb-3">Detalle de la Factura</h5>
                    <div class="overflow-x-auto">
                        <table class="min-w-full">
                            <thead class="bg-gray-100">
                                <tr>
                                    <th class="py-2 px-3 text-left text-sm font-medium text-gray-700">Descripción</th>
                                    <th class="py-2 px-3 text-center text-sm font-medium text-gray-700">Cant.</th>
                                    <th class="py-2 px-3 text-right text-sm font-medium text-gray-700">Precio Unit.</th>
                                    <th class="py-2 px-3 text-right text-sm font-medium text-gray-700">Subtotal</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm">
                                ${itemsHtml}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Totales -->
                <div class="border-t border-gray-300 pt-4">
                    <div class="flex justify-end">
                        <div class="w-64 space-y-2">
                            <div class="flex justify-between">
                                <span>Subtotal:</span>
                                <span>$${factura.subtotal.toLocaleString('es-CO')} COP</span>
                            </div>
                            <div class="flex justify-between">
                                <span>IVA (19%):</span>
                                <span>$${factura.iva.toLocaleString('es-CO')} COP</span>
                            </div>
                            <div class="flex justify-between font-bold text-lg border-t pt-2">
                                <span>TOTAL:</span>
                                <span>$${factura.total.toLocaleString('es-CO')} COP</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Validación del formulario
    const form = document.getElementById('facturaForm');
    form.addEventListener('submit', function(e) {
        const numeroFactura = numeroFacturaInput.value.trim();
        if (!numeroFactura) {
            e.preventDefault();
            alert('Por favor, ingresa un número de factura');
            numeroFacturaInput.focus();
        }
    });
});
