// ISBN Converter by Ken SATO
// LICENSE: GPLv3

public class ISBNConverter {

	public static void main(String[] args) {

		// remove '-' characters from args[0] 
		// Note: Anywhere, Any numbers of Hyphen can be accepted. 
		String isbn = args[0].replaceAll("-", "");

		// ISBN10 validation
		if (isbn.length()!=10) {
			System.out.println(isbn + " is not ISBN10 obviously.");
			System.exit(0);
		}

		// String to char to int conversion
		char [] cisbn = isbn.toCharArray();
		int [] iisbn;
		iisbn = new int[10];
	
		// check for iisbn[0 to 8] which is the first 9 numbers
		// Note: Strictly check the numbers.
		for (int idx=0; idx<9; idx++) {
			iisbn[idx] = Character.digit(cisbn[idx], 10);
			if ((iisbn[idx]<0)||(iisbn[idx]>9)){
				System.out.println("Error: Not a number is included in the 9 numbers.");
				System.exit(0);
			}
		}
		
		// check for iisbn[9] which is the checkdigit
		// Note: Strictly check the number.
		if (cisbn[9] == 'X'){
			iisbn[9] = 10;
		}
		else {
			iisbn[9] = Character.digit(cisbn[9], 10);			
			if ((iisbn[9]<0)||(iisbn[9]>9)){
				System.out.println("Error: Not a number or X is included in the checkdigit.");
				System.exit(0);
			}
		}
			
		// calc and check the checkdigit
		int cdigit = 0;
		for (int idx=0; idx<9; idx++){
			cdigit = cdigit + (10-idx)*iisbn[idx];
		}
		cdigit = cdigit % 11;
		cdigit = 11 - cdigit;
		
		if (cdigit != iisbn[9]){
			System.out.println("Error: Invalid checkdigit.");
			System.exit(0);
		}
		
		// calc new(for ISBN13) checkdigit
		int ncdigit = 0;
		ncdigit = 9*1 + 7*3 + 8*1;
		for (int idx=0; idx<4; idx++){
			ncdigit = ncdigit + 3*iisbn[idx*2] + iisbn[idx*2+1];
		}
		ncdigit = ncdigit + 3*iisbn[8];
		ncdigit = ncdigit % 10;
		ncdigit = 10 - ncdigit;
		
		// Convert int to String for ISBN13 checkdigit
		String lastx = String.valueOf(ncdigit);
		
		// result output
		System.out.println("ISBN10: " + isbn);
		System.out.println("ISBN13: " + "978" + isbn.substring(0, 9) + lastx);
	}
