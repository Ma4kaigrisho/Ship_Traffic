import socket
import time

def gga(MessageID: str, UTCTime: str, Latitude: float, NSIndicator: str, Longitude: float, EWIndicator: str, PositionFixIndicator: int, SatellitesUsed: int, HDOP: float, MSLAltitude: float, Units: str, GeoidSeparation: float, AgeofDiffCorr: float, DiffRefStationID: str, Checksum: str):
    AgeofDiffCorr = "" if AgeofDiffCorr is None else str(AgeofDiffCorr)
    return f"{MessageID},{UTCTime},{Latitude},{NSIndicator},{Longitude},{EWIndicator},{PositionFixIndicator},{SatellitesUsed},{HDOP},{MSLAltitude},{Units},{GeoidSeparation},{Units},{AgeofDiffCorr},{DiffRefStationID}{Checksum}"
    

def gll(MessageID: str, Latitude: float, NSIndicator: str, Longitude: float, EWIndicator: str, UTCTime: str, Status: str, Mode: str, Checksum: str):
    return f"{MessageID},{Latitude},{NSIndicator},{Longitude},{EWIndicator},{UTCTime},{Status},{Mode}{Checksum}"

def gsa(MessageID: str, Mode1: str, Mode2: str, SatellitesUsed1: str, SatellitesUsed2: str, SatellitesUsed3: str, SatellitesUsed4: str, SatellitesUsed5: str, SatellitesUsed6: str, SatellitesUsed7: str, SatellitesUsed8: str, SatellitesUsed9: str, SatellitesUsed10: str, SatellitesUsed11: str, SatellitesUsed12: str, PDOP: str, HDOP: str, VDOP: str, Checksum: str):
    return f"{MessageID},{Mode1},{Mode2},{SatellitesUsed1},{SatellitesUsed2},{SatellitesUsed3},{SatellitesUsed4},{SatellitesUsed5},{SatellitesUsed6},{SatellitesUsed7},{SatellitesUsed8},{SatellitesUsed9},{SatellitesUsed10},{SatellitesUsed11},{SatellitesUsed12},{PDOP},{HDOP},{VDOP}{Checksum}"
def gsv():
    return
def send_nmea_messages(client_socket):
    while True:
        message_type = input("Enter NMEA message type (GGA/GLL,GSA): ").upper()

        if message_type == 'GGA':
            parameters = input("Enter GGA parameters (UTCTime,Latitude,NSIndicator,Longitude,EWIndicator,PositionFixIndicator,SatellitesUsed,HDOP,MSLAltitude,Units,GeoidSeparation,AgeofDiffCorr,DiffRefStationID,Checksum): ")
            nmea_message = gga("$GPGGA", *parameters.split(','))
        elif message_type == 'GLL':
            parameters = input("Enter GLL parameters (Latitude,NSIndicator,Longitude,EWIndicator,UTCTime,Status,Mode,Checksum): ")
            nmea_message = gll("$GPGLL", *parameters.split(','))
        elif message_type == 'GSA':
            parameters = input("Enter GSA parameters (Mode1,Mode2,Satelites Used(1-12),PDOP,HDOP,VDOP,Checksum)")
            nmea_message=gsa("$GPGSA",*parameters.split(','))
        else:
            print("Invalid message type. Please enter GGA or GLL.")
            continue

        client_socket.sendall((nmea_message + "\r\n").encode())
        time.sleep(1)

def main():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            send_nmea_messages(conn)

if __name__ == "__main__":
    main()