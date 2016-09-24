/*
*@file ejemplo_pcap
*@brief Programa que permite capturar paquetes, ya sea uno o
*      indefinidos y lo muestra en pantalla
*@author Vilchis Domínguez Miguel Alonso
*@version 1.0
*/

/*++++++++++++++++Compilacion y uso +++++++++++++++++++++++++
  *Para instalar libpcap: apt-get install libpcap-dev
 *Para compilar el programa la linea de comandos corrrespondiente
 *es: gcc ejemplo_pcap.c -o lab -lpcap
 *Y como super usuario se ejecuta ./lab
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */

 #include <stdio.h>
 #include <stdlib.h>
 #include <pcap.h>
 #include <arpa/inet.h>
 #include "ejemplo_pcap.h"



 /**************************************************************
 *
 *@brief Funcion que será llamada si queremos capturar solo un
 *       paquete
 *
 ***************************************************************/

 int opcionUnPaquete () {
     //Obtenemos interfaz disponible
     char errbuf[PCAP_ERRBUF_SIZE];
     char *dev;
     const struct ip_header *ip;
     pcap_t *captura;
     const u_char *paquete;
     struct pcap_pkthdr h;


     dev = pcap_lookupdev(errbuf);
     //Si el apuntador a dispositivo de red no es válido, no continuamos
     if(dev ==NULL) {
         printf("En dispositivo de red ERROR: %s\n", errbuf);
         return EXIT_FAILURE;
     }
     //Imprimimos el dispositivo de red
     printf("Capturaremos del dispositivo: %s \n", dev);
     //Abrimos la interfaz de red
     captura = pcap_open_live(dev,BUFSIZ,1,1000, errbuf);
     //Si la captura no fue exitosa salimos del programa
     if(captura== NULL) {
         printf("En captura ERROR: %s\n", errbuf);
         return EXIT_FAILURE;
     }
     //Capturamos un paquete
     paquete = pcap_next(captura, &h);
     //Si ocurrió un error al recibir un paquete salimos
     if(paquete == NULL) {
         printf("Al recibir un paquete ERROR: %s \n",errbuf);
         return EXIT_FAILURE;
     }
     printf("Imprimimos el paquete\n");
     int i;
     for(i = 0;i < h.len; i++) {
         printf("%x ", paquete[i]);
     }
     printf("\n");

     ip = (struct ip_header*)(paquete + TAM_ETHERNET);
     printf("(%x )%s -> (%x)%s \n",ip -> ip_src, inet_ntoa(ip->ip_src),((*ip).ip_dst),inet_ntoa(ip->ip_dst));
     printf("Protocolo :%x", ip->ip_p);

     return EXIT_SUCCESS;
 }

 int main () {
    //Dado que al tratar de usar una interfaz de red disponible
    //Libpcap busca usa la primera, entonces la siguiente secuencia
    //Nos indica cual es la primera.
    /*
    char ebuf[PCAP_ERRBUF_SIZE];
    pcap_if_t* deviceList;
    pcap_if_t* d;
    printf("%i \n",pcap_findalldevs(&deviceList,ebuf));
    while(deviceList->next != NULL ) {
        printf("%s \n",(deviceList->name));
        deviceList = deviceList->next;
    }
    */
    opcionUnPaquete();
    //Para varios paquetes :
    //revisar: pcap_loop(captura,-1,callback, NULL);
    return 0;
}